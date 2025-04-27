from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail

from .models import Pokemon
import random


# ALL_STARTERS = [
#     "Bulbasaur", "Charmander", "Squirtle",
#     "Chikorita", "Cyndaquil", "Totodile",
#     "Treecko", "Torchic", "Mudkip",
#     "Turtwig", "Chimchar", "Piplup",
#     "Snivy", "Tepig", "Oshawott",
#     "Chespin", "Fennekin", "Froakie",
#     "Rowlet", "Litten", "Popplio",
#     "Grookey", "Scorbunny", "Sobble",
#     "Sprigatito", "Fuecoco", "Quaxly"
# ]


def index(request):
    return render(request, 'home/index.html');


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
    starters = request.session.get('starter_choices')
    if not starters:
        return redirect('dashboard')  # fallback if someone skips registration
    if request.method == 'POST':
        selected = request.POST.get('starter')
        if selected in starters:
            request.user.profile.starter_pokemon = selected
            request.user.profile.save()
            del request.session['starter_choices']  # clear from session
            return redirect('dashboard')
    return render(request, 'home/choose_starter.html', {'starters': starters})



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
    pokemons = Pokemon.objects.order_by('poke_id')
    return render(request, 'home/marketplace.html', {
        'pokemon_list': pokemons
    })

def collection(request):
    return render(request, 'home/collection.html')

def trade(request):
    return render(request, 'home/trade.html')

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

