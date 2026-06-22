import requests


def get_steam_inventory(steam_id):
    games = {
        'CS2': 730,
        'Dota 2': 570,
        'Rust': 252490,
    }
    result = {}
    for game_name, app_id in games.items():
        url = f'https://steamcommunity.com/inventory/{steam_id}/{app_id}/2'
        params = {'l': 'ukrainian', 'count': 50}
        try:
            resp = requests.get(url, params=params, timeout=5)
            data = resp.json()
            items = []
            if data.get('assets') and data.get('descriptions'):
                desc_map = {
                    (d['classid'], d['instanceid']): d
                    for d in data['descriptions']
                }
                for asset in data['assets']:
                    desc = desc_map.get((asset['classid'], asset['instanceid']))
                    if desc:
                        items.append({
                            'name': desc.get('name'),
                            'image': f"https://community.akamai.steamstatic.com/economy/image/{desc.get('icon_url')}",
                            'rarity_color': desc.get('name_color', 'b0c3d9'),
                            'tradable': desc.get('tradable', 0),
                            'type': desc.get('type', ''),
                        })
            result[game_name] = items
        except Exception:
            result[game_name] = []
    return result
