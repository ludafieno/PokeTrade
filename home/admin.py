from django.contrib import admin
from .models import Profile, Pokemon, Report
from django import forms

from .utils import fetch_pokemon


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display    = ('poke_id', 'name')
    fields          = ('poke_id','name','sprite','types','description','health')
    readonly_fields = ('name','sprite','types','description','health')

    def save_model(self, request, obj, form, change):
        # On create or when poke_id is changed, fetch fresh data
        if not change or 'poke_id' in form.changed_data:
            data = fetch_pokemon(obj.poke_id)
            obj.name        = data['name']
            obj.sprite      = data['sprite']
            obj.types       = data['types']
            obj.description = data['description']
            obj.health      = data['health']
        super().save_model(request, obj, form, change)

admin.site.register(Report)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def clean_starter_pokemon(self):
        val = self.cleaned_data.get('starter_pokemon')
        # Convert empty ('') to None so the field can accept it
        if val in (None, ''):
            return None
        return val

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileForm
    list_display = ['user']
    filter_horizontal = ('collection',)