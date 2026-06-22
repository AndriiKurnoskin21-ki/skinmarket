from django.db import migrations


def seed_games(apps, schema_editor):
    Game = apps.get_model('skins', 'Game')
    games = [
        {'name': 'Dota 2', 'slug': 'dota2', 'icon': '🏆', 'color': '#FF6B35'},
        {'name': 'CS2',    'slug': 'cs2',   'icon': '🔫', 'color': '#FFD700'},
        {'name': 'Rust',   'slug': 'rust',  'icon': '🪓', 'color': '#CD4B2C'},
    ]
    for g in games:
        Game.objects.get_or_create(slug=g['slug'], defaults=g)


def remove_games(apps, schema_editor):
    Game = apps.get_model('skins', 'Game')
    Game.objects.filter(slug__in=['dota2', 'cs2', 'rust']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('skins', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_games, remove_games),
    ]
