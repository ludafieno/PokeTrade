from django.http import HttpResponse
from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail

from .forms import TradeForm
from .models import Pokemon, Profile
from collections import Counter
import random

from .utils import fetch_pokemon

ALL_STARTERS = [
    1, 4, 7,
    152, 155, 158,
    252, 255, 258,
    387, 390, 393,
    495, 498, 451,
    650, 653, 656,
    722, 725, 728,
    810, 813, 816,
]

def index(request):
    return render(request, 'home/index.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)

            # Save 3 random starters in session
            request.session['starter_choices'] = random.sample(ALL_STARTERS, 3)

            return redirect('choose_starter')
    else:
        form = UserCreationForm()
    return render(request, 'home/register.html', {'form': form})

@login_required
def choose_starter(request):
    if 'starter_choices' not in request.session:
        request.session['starter_choices'] = random.sample(ALL_STARTERS, 3)
    starter_ids = request.session['starter_choices']

    if request.method == 'POST':
        selected = request.POST.get('starter')
        if selected and selected.isdigit():
            selected_id = int(selected)
            if selected_id in starter_ids:
                profile = get_object_or_404(Profile, user=request.user)

                # Fetch full data from API
                data = fetch_pokemon(selected_id)
                # Remove poke_id from defaults so get_or_create matches only on the lookup field
                poke_defaults = {
                    'name': data['name'],
                    'sprite': data['sprite'],
                    'types': data['types'],
                    'description': data['description'],
                    'health': data['health'],
                }
                pokemon_obj, created = Pokemon.objects.get_or_create(
                    poke_id=selected_id,
                    defaults=poke_defaults
                )
                # Add to the user’s M2M collection
                profile.collection.add(pokemon_obj)

                # Prevent re-selection
                del request.session['starter_choices']
                return redirect('dashboard')

        # --- 3) On GET (or invalid POST), build exactly three cards ---
    starters = []
    for pid in starter_ids:
        try:
            info = fetch_pokemon(pid)
        except Exception:
            info = {
                'poke_id': pid,
                'name': f'Pokémon #{pid}',
                'sprite': '',
                'types': [],
                'description': '',
                'health': 0,
            }
        starters.append(info)

    return render(request, 'home/choose_starter.html', {
        'starters': starters
    })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))
    else:
       form = AuthenticationForm()
    return render(request, 'home/login.html', {'form': form})

def about(request):
    return render(request, 'home/about.html')

@login_required
def dashboard(request):
    return render(request, 'home/dashboard.html')

def marketplace(request):
    pokemons = Pokemon.objects.order_by('id')
    return render(request, 'home/marketplace.html', {
        'pokemon_list': pokemons
    })

def collection(request):
    profile = request.user.profile
    pokemons = profile.collection.all()
    total = pokemons.count()

    # Find favorite type
    all_types = [t for p in pokemons for t in (p.types or [])]
    fav = Counter(all_types).most_common(1)
    fav_type = fav[0][0] if fav else "None"

    return render(request, 'home/collection.html', {
        'total': total,
        'fav_type': fav_type,
        'pokemons': pokemons,
    })

@login_required
def trade(request):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            trade = form.save(commit=False)
            trade.sender = request.user
            trade.save()

            profile = request.user.profile
            if profile.currency >= 50:
                profile.currency -= 50
                profile.save()
            else:

                trade.delete()
                return HttpResponse("Not enough coins to send a trade!")

            return redirect('dashboard')
    else:
        form = TradeForm()

    form.fields['offered_pokemon'].queryset = request.user.profile.collection.all()
    form.fields['requested_pokemon'].queryset = Pokemon.objects.exclude(owners=request.user.profile)

    return render(request, 'home/trade.html', {'form': form})

@login_required
def report_issue(request):
    if request.method == 'POST':
        issue_type = request.POST.get('issue_type')
        description = request.POST.get('description')
        subject = f"New {issue_type.capitalize()} Report from {request.user.username}"
        message = f"Issue Type: {issue_type}\nUser: {request.user.username}\n\nDescription:\n{description}"

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])

        return redirect('dashboard')  # or a success page

    return render(request, 'report.html')
def logout_view(request):
    logout(request)
    return redirect('index')

