"""
python manage.py setup_games

Автоматично створює Dota 2, CS2, Rust з правильними Steam App ID.
Викликається автоматично з AppConfig.ready() при першому запуску.
"""
from django.core.management.base import BaseCommand


GAMES = [
    {
        'name':             'CS2',
        'slug':             'cs2',
        'icon':             '🔫',
        'color':            '#FFD700',
        'steam_app_id':     730,
        'steam_context_id': 2,
    },
    {
        'name':             'Dota 2',
        'slug':             'dota2',
        'icon':             '🏆',
        'color':            '#FF6B35',
        'steam_app_id':     570,
        'steam_context_id': 2,
    },
    {
        'name':             'Rust',
        'slug':             'rust',
        'icon':             '🪓',
        'color':            '#CD4B2C',
        'steam_app_id':     252490,
        'steam_context_id': 2,
    },
]


class Command(BaseCommand):
    help = 'Створює 3 гри (CS2, Dota 2, Rust) якщо їх ще немає'

    def handle(self, *args, **options):
        from skins.models import Game
        created_count = 0
        for data in GAMES:
            _, created = Game.objects.get_or_create(
                slug=data['slug'],
                defaults=data,
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  ✅ Створено: {data['name']}"))
            else:
                self.stdout.write(f"  ⏭ Вже існує: {data['name']}")

        self.stdout.write(self.style.SUCCESS(
            f'\nГотово! Створено {created_count} нових ігор.'
        ))
