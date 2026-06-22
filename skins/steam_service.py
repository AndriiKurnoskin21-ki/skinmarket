"""
skins/steam_service.py
Тягне інвентар Steam і імпортує скіни в БД.
"""
import requests
from decimal import Decimal
from .models import Game, Skin

STEAM_INVENTORY_URL = (
    'https://steamcommunity.com/inventory/{steam_id}/{app_id}/{context_id}'
    '?l=english&count=75'
)

RARITY_MAP = {
    # CS2
    'Rarity_Common_Weapon':     'consumer',
    'Rarity_Uncommon_Weapon':   'industrial',
    'Rarity_Rare_Weapon':       'mil_spec',
    'Rarity_Mythical_Weapon':   'restricted',
    'Rarity_Legendary_Weapon':  'classified',
    'Rarity_Ancient_Weapon':    'covert',
    'Rarity_Contraband':        'contraband',
    # Dota 2
    'Rarity_Common':            'consumer',
    'Rarity_Uncommon':          'industrial',
    'Rarity_Rare':              'restricted',
    'Rarity_Mythical':          'classified',
    'Rarity_Legendary':         'covert',
    'Rarity_Immortal':          'immortal',
    'Rarity_Arcana':            'arcana',
}

CONDITION_MAP = {
    'Factory New':    'fn',
    'Minimal Wear':   'mw',
    'Field-Tested':   'ft',
    'Well-Worn':      'ww',
    'Battle-Scarred': 'bs',
}


def _parse_condition(name: str):
    for label, code in CONDITION_MAP.items():
        if f'({label})' in name:
            return code
    return ''


def _parse_rarity(tags: list):
    for tag in tags:
        if tag.get('category') == 'Rarity':
            internal = tag.get('internal_name', '')
            return RARITY_MAP.get(internal, 'consumer')
    return 'consumer'


def _steam_image(icon_url: str) -> str:
    if not icon_url:
        return ''
    return f'https://community.akamai.steamstatic.com/economy/image/{icon_url}/360fx360f'


def import_inventory(user, game: Game, default_price: Decimal = Decimal('9.99')) -> dict:
    """
    Тягне Steam-інвентар користувача для вказаної гри та додає/оновлює Skin-и.
    Повертає {'imported': N, 'skipped': M, 'errors': [...]}
    """
    try:
        steam_profile = user.steam_profile
    except Exception:
        return {'imported': 0, 'skipped': 0, 'errors': ['Не знайдено Steam профілю. Увійдіть через Steam.']}

    url = STEAM_INVENTORY_URL.format(
        steam_id=steam_profile.steam_id,
        app_id=game.steam_app_id,
        context_id=game.steam_context_id,
    )

    try:
        resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return {'imported': 0, 'skipped': 0, 'errors': [f'Steam API помилка: {e}']}

    if not data.get('success'):
        return {'imported': 0, 'skipped': 0, 'errors': ['Steam повернув success=false. Перевірте приватність інвентаря.']}

    assets       = {a['assetid']: a for a in data.get('assets', [])}
    descriptions = {(d['classid'], d.get('instanceid', '0')): d for d in data.get('descriptions', [])}

    imported = 0
    skipped  = 0
    errors   = []

    for asset_id, asset in assets.items():
        key = (asset['classid'], asset.get('instanceid', '0'))
        desc = descriptions.get(key)
        if not desc:
            skipped += 1
            continue

        if not desc.get('tradable', 0):
            skipped += 1
            continue

        name      = desc.get('market_name') or desc.get('name', 'Unknown')
        icon_url  = desc.get('icon_url', '')
        tags      = desc.get('tags', [])
        rarity    = _parse_rarity(tags)
        condition = _parse_condition(name)
        image_url = _steam_image(icon_url)

        # Опис зі Steam
        descriptions_text = ''
        for d in desc.get('descriptions', []):
            val = d.get('value', '').strip()
            if val and val != ' ':
                descriptions_text += val + '\n'

        _, created = Skin.objects.get_or_create(
            seller=user,
            game=game,
            steam_asset_id=asset_id,
            defaults={
                'name':           name,
                'steam_class_id': asset['classid'],
                'image_url':      image_url,
                'description':    descriptions_text.strip(),
                'rarity':         rarity,
                'condition':      condition,
                'price':          default_price,
                'is_listed':      True,
            }
        )
        if created:
            imported += 1
        else:
            skipped += 1

    return {'imported': imported, 'skipped': skipped, 'errors': errors}
