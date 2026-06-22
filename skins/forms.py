from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Skin, Review, UserProfile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class SkinForm(forms.ModelForm):
    class Meta:
        model = Skin
        fields = ['game', 'name', 'description', 'price', 'image', 'image_url',
                  'rarity', 'condition', 'float_value']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-input'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-input'}),
            'text': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
        }
        labels = {'rating': 'Оцінка', 'text': 'Відгук'}


class NewsletterForm(forms.Form):
    email = forms.EmailField(
        label='Ваш Email',
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'your@email.com'})
    )
    name = forms.CharField(
        max_length=100, label="Ваше ім'я",
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': "Ваше ім'я"})
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['steam_id', 'steam_trade_url']
        widgets = {
            'steam_id': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '76561198XXXXXXXXX'
            }),
            'steam_trade_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://steamcommunity.com/tradeoffer/new/?partner=...&token=...'
            }),
        }
        labels = {
            'steam_id': 'Steam ID (17 цифр)',
            'steam_trade_url': 'Steam Trade Link',
        }
