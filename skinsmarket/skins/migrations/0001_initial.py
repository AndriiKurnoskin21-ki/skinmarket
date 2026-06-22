from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('icon', models.CharField(default='🎮', max_length=10)),
                ('color', models.CharField(default='#FF6B35', max_length=7)),
                ('image', models.ImageField(blank=True, null=True, upload_to='games/')),
            ],
            options={'verbose_name': 'Гра', 'verbose_name_plural': 'Ігри'},
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('steam_trade_url', models.URLField(blank=True, verbose_name='Steam Trade Link')),
                ('steam_id', models.CharField(blank=True, help_text='17-значний Steam ID. Знайти на steamid.io', max_length=20, verbose_name='Steam ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='auth.user')),
            ],
            options={'verbose_name': 'Профіль', 'verbose_name_plural': 'Профілі'},
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Очікує'), ('paid', 'Оплачено'), ('completed', 'Завершено'), ('cancelled', 'Скасовано')], default='pending', max_length=20)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='auth.user')),
            ],
            options={'verbose_name': 'Замовлення', 'verbose_name_plural': 'Замовлення', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Skin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='skins/')),
                ('image_url', models.URLField(blank=True)),
                ('rarity', models.CharField(choices=[('consumer', 'Consumer Grade'), ('industrial', 'Industrial Grade'), ('mil_spec', 'Mil-Spec'), ('restricted', 'Restricted'), ('classified', 'Classified'), ('covert', 'Covert'), ('extraordinary', 'Extraordinary'), ('common', 'Common (Rust)'), ('uncommon', 'Uncommon (Rust)'), ('rare', 'Rare (Rust)'), ('epic', 'Epic (Rust)'), ('legendary', 'Legendary (Rust)')], default='consumer', max_length=20)),
                ('condition', models.CharField(blank=True, choices=[('fn', 'Factory New'), ('mw', 'Minimal Wear'), ('ft', 'Field-Tested'), ('ww', 'Well-Worn'), ('bs', 'Battle-Scarred')], max_length=5)),
                ('status', models.CharField(choices=[('available', 'Доступний'), ('sold', 'Продано'), ('reserved', 'Зарезервовано')], default='available', max_length=20)),
                ('float_value', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('views', models.PositiveIntegerField(default=0)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skins', to='skins.game')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skins', to='auth.user')),
            ],
            options={'verbose_name': 'Скін', 'verbose_name_plural': 'Скіни', 'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('skin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='skins.skin')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={'verbose_name': 'Відгук', 'verbose_name_plural': 'Відгуки', 'unique_together': {('skin', 'author')}},
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='skins.order')),
                ('skin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skins.skin')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='skins.cart')),
                ('skin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='skins.skin')),
            ],
            options={'unique_together': {('cart', 'skin')}},
        ),
    ]
