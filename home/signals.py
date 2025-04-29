import random
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile, Pokemon
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.contrib import messages
from .utils   import fetch_pokemon


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

receiver(user_logged_in)
def give_daily_reward(sender, user, request, **kwargs):
    profile = user.profile
    today   = timezone.localdate()

    # Only once per calendar day
    if profile.daily_reward != today:
        # 1) Grant 100 PokéCoins
        profile.currency += 100

        # 2) Pick a random Gen-I Pokémon ID
        pid = random.randint(1, 151)

        # 3) Fetch its data & create a new card, assigning ownership
        data = fetch_pokemon(pid)
        new_card = Pokemon.objects.create(
            owner       = profile,
            poke_id     = pid,
            name        = data['name'],
            sprite      = data['sprite'],
            types       = data['types'],
            description = data['description'],
            health      = data['health']
        )

        # 4) (Optional) keep your old M2M collection in sync
        profile.collection.add(new_card)

        # 5) Mark the reward claimed for today
        profile.daily_reward = today
        profile.save(update_fields=['currency', 'daily_reward'])

        messages.success(
            request,
            f"🎉 You’ve earned 100 PokéCoins and a random Gen I Pokémon: {data['name']}!"
        )
    else:
        messages.info(request, "You’ve already claimed your daily reward today. Come back tomorrow!")