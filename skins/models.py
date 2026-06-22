from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Рідкості згруповані по іграх — використовуються у views і шаблонах
RARITY_BY_GAME = {
    'cs2': [
        ('consumer',      'Consumer Grade'),
        ('industrial',    'Industrial Grade'),
        ('mil_spec',      'Mil-Spec'),
        ('restricted',    'Restricted'),
        ('classified',    'Classified'),
        ('covert',        'Covert'),
        ('extraordinary', 'Extraordinary'),
    ],
    'dota2': [
        ('common',        'Common'),
        ('uncommon',      'Uncommon'),
        ('rare',          'Rare'),
        ('mythical',      'Mythical'),
        ('legendary',     'Legendary'),
        ('immortal',      'Immortal'),
        ('arcana',        'Arcana'),
    ],
    'rust': [
        ('common',        'Common'),
        ('uncommon',      'Uncommon'),
        ('rare',          'Rare'),
        ('epic',          'Epic'),
        ('legendary',     'Legendary'),
    ],
}

# Плоский список для поля моделі (всі унікальні значення)
RARITY_CHOICES = []
_seen = set()
for _choices in RARITY_BY_GAME.values():
    for _value, _label in _choices:
        if _value not in _seen:
            RARITY_CHOICES.append((_value, _label))
            _seen.add(_value)


class Game(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10, default='🎮')
    color = models.CharField(max_length=7, default='#FF6B35')
    image = models.ImageField(upload_to='games/', blank=True, null=True)

    class Meta:
        verbose_name = 'Гра'
        verbose_name_plural = 'Ігри'

    def __str__(self):
        return self.name


class Skin(models.Model):
    CONDITION_CHOICES = [
        ('fn', 'Factory New'),
        ('mw', 'Minimal Wear'),
        ('ft', 'Field-Tested'),
        ('ww', 'Well-Worn'),
        ('bs', 'Battle-Scarred'),
    ]

    STATUS_CHOICES = [
        ('available', 'Доступний'),
        ('sold', 'Продано'),
        ('reserved', 'Зарезервовано'),
    ]

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='skins')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skins')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='skins/', blank=True, null=True)
    image_url = models.URLField(blank=True, max_length=500)
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, default='common')
    condition = models.CharField(max_length=5, choices=CONDITION_CHOICES, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    float_value = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Скін'
        verbose_name_plural = 'Скіни'

    def __str__(self):
        return f'{self.name} ({self.game.name})'

    def get_absolute_url(self):
        return reverse('skin_detail', args=[self.pk])

    def get_rarity_choices_for_game(self):
        """Повертає список рідкостей для гри цього скіна."""
        return RARITY_BY_GAME.get(self.game.slug, RARITY_CHOICES)

    @property
    def rarity_color(self):
        colors = {
            'consumer':      '#b0c3d9',
            'industrial':    '#5e98d9',
            'mil_spec':      '#4b69ff',
            'restricted':    '#8847ff',
            'classified':    '#d32ce6',
            'covert':        '#eb4b4b',
            'extraordinary': '#e4ae39',
            'common':        '#b0b0b0',
            'uncommon':      '#4caf50',
            'rare':          '#3399ff',
            'mythical':      '#8847ff',
            'epic':          '#a335ee',
            'legendary':     '#ff8c00',
            'immortal':      '#eb4b4b',
            'arcana':        '#ff4444',
        }
        return colors.get(self.rarity, '#ffffff')
