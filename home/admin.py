from django.contrib import admin
from django.shortcuts import get_object_or_404

from .models import Profile, Pokemon, Report, Trade, Listing
from django import forms
from django.contrib import admin
from .utils import fetch_pokemon


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display    = ('poke_id','name','owner')
    fields          = ('owner','poke_id','name','sprite','types',
                       'description','health','attack','defense',
                       'special_attack','special_defense','speed')
    readonly_fields = ('name','sprite','types','description',
                       'health','attack','defense',
                       'special_attack','special_defense','speed')

    def save_model(self, request, obj, form, change):
        # whenever it's new or you change poke_id, re-fetch everything
        if not change or 'poke_id' in form.changed_data:
            data = fetch_pokemon(obj.poke_id)

            # build a lookup: stat_name -> base_stat
            stat_map = {
                stat_block['stat']['name']: stat_block['base_stat']
                for stat_block in data['stats']
            }

            # assign each field
            obj.name            = data['name']
            obj.sprite          = data['sprite']
            obj.types           = data['types']
            obj.description     = data['description']

            obj.health          = stat_map.get('hp', 0)
            obj.attack          = stat_map.get('attack', 0)
            obj.defense         = stat_map.get('defense', 0)
            obj.special_attack  = stat_map.get('special-attack', 0)
            obj.special_defense = stat_map.get('special-defense', 0)
            obj.speed           = stat_map.get('speed', 0)

        old_owner = None
        if change:
            old_owner = Pokemon.objects.get(pk=obj.pk).owner

        super().save_model(request, obj, form, change)

        # 3) Sync the M2M on the new owner
        if obj.owner:
            obj.owner.collection.add(obj)

        # 4) If owner changed, remove from the old owner's collection
        if old_owner and old_owner != obj.owner:
            old_owner.collection.remove(obj)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'report_type', 'created_at')
    list_filter  = ('report_type',)


# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = '__all__'
#
#     def clean_starter_pokemon(self):
#         val = self.cleaned_data.get('starter_pokemon')
#         # Convert empty ('') to None so the field can accept it
#         if val in (None, ''):
#             return None
#         return val


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'currency', 'daily_reward')
    filter_horizontal = ('collection',)
    exclude = ('pokemons',)

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'offered_pokemon', 'requested_pokemon', 'is_accepted', 'is_approved_by_admin', 'created_at')
    list_editable = ('is_approved_by_admin',)
    list_filter = ('is_accepted', 'is_approved_by_admin')
    search_fields = ('sender__username', 'receiver__username')


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display  = ("pokemon", "seller", "price", "created_at")
    list_filter   = ("seller",)
    search_fields = ("pokemon__name", "seller__user__username")