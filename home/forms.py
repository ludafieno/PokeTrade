from django import forms
from .models import Trade, Profile


class TradeForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ['offered_pokemon', 'requested_pokemon']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
