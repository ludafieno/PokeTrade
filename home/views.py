from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail



def index(request):
    return render(request, 'home/index.html');

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'home/register.html', {'form': form})


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
    return render(request, 'home/marketplace.html')

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

