from django.contrib import admin
from .models import Report
from .models import Pokemon

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

# Register your models here.
