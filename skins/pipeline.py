"""
skins/pipeline.py
Кастомний крок social-auth: зберігає Steam-профіль після логіну.
"""
import requests
from .models import SteamProfile


def save_steam_profile(backend, user, response, *args, **kwargs):
    """Тягнемо публічний профіль Steam і зберігаємо в SteamProfile."""
    if backend.name != 'steam':
        return

    steam_id = response.get('steamid') or kwargs.get('uid', '')

    # Намагаємось отримати аватар/нікнейм через Steam API (якщо є ключ)
    persona_name = response.get('personaname', user.username)
    avatar_url   = response.get('avatarfull', '')
    profile_url  = response.get('profileurl', '')

    SteamProfile.objects.update_or_create(
        steam_id=steam_id,
        defaults={
            'user': user,
            'persona_name': persona_name,
            'avatar_url': avatar_url,
            'profile_url': profile_url,
        }
    )
