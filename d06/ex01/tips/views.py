import random
import time
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm

User = get_user_model()


def get_or_refresh_anon_name(request):
    now = time.time()
    expire_at = request.session.get('anon_expire_at', 0)
    if now > expire_at:
        name = random.choice(settings.ANONYMOUS_NAMES)
        request.session['anon_name'] = name
        request.session['anon_expire_at'] = now + 42
    return request.session['anon_name']


def home(request):
    anon_name = get_or_refresh_anon_name(request)
    return render(request, 'tips/home.html', {'anon_name': anon_name})


def register_view(request):
    """Ex01 : Inscription. Redirige vers home si déjà connecté."""
    if request.user.is_authenticated:
        return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        login(request, user)
        return redirect('home')
    return render(request, 'tips/register.html', {'form': form})


def login_view(request):
    """Ex01 : Connexion. Redirige vers home si déjà connecté."""
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(request.POST or None)
    error = None
    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('home')
            else:
                error = "Identifiants incorrects."
    return render(request, 'tips/login.html', {'form': form, 'error': error})


def logout_view(request):
    """Ex01 : Déconnexion + redirection vers home."""
    logout(request)
    return redirect('home')
