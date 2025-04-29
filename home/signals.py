from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile, Pokemon
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
import random
from django.contrib import messages


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(user_logged_in)
def give_daily_reward(sender, user, request, **kwargs):
    today = timezone.now().date()
    profile = user.profile

    if profile.daily_reward != today:
        profile.currency += 100

        gen1_pokemon = Pokemon.objects.filter(poke_id__gte=1, poke_id__lte=151)
        if gen1_pokemon.exists():
            random_pokemon = random.choice(list(gen1_pokemon))
            profile.collection.add(random_pokemon)

        profile.daily_reward = today
        profile.save()
        messages.success(request, "🎉 You earned 100 PokéCoins and 1 Pokémon today!")