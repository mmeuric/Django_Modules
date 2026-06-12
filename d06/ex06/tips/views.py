import random, time
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, LoginForm, TipForm
from .models import Tip

User = get_user_model()


def get_or_refresh_anon_name(request):
    now = time.time()
    if now > request.session.get('anon_expire_at', 0):
        name = random.choice(settings.ANONYMOUS_NAMES)
        request.session['anon_name'] = name
        request.session['anon_expire_at'] = now + 42
    return request.session['anon_name']


def home(request):
    anon_name = get_or_refresh_anon_name(request)
    tips = Tip.objects.all()
    tip_form = None
    if request.user.is_authenticated:
        tip_form = TipForm(request.POST or None)
        if request.method == 'POST' and tip_form.is_valid():
            tip = tip_form.save(commit=False)
            tip.auteur = request.user
            tip.save()
            return redirect('home')
    return render(request, 'tips/home.html', {
        'anon_name': anon_name, 'tips': tips, 'tip_form': tip_form
    })


def register_view(request):
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
    if request.user.is_authenticated:
        return redirect('home')
    form = LoginForm(request.POST or None)
    error = None
    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])
            if user:
                login(request, user); return redirect('home')
            else:
                error = "Identifiants incorrects."
    return render(request, 'tips/login.html', {'form': form, 'error': error})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def upvote(request, tip_id):
    tip = get_object_or_404(Tip, id=tip_id)
    user = request.user
    if user in tip.upvoters.all():
        tip.upvoters.remove(user)
    else:
        tip.downvoters.remove(user)
        tip.upvoters.add(user)
    return redirect('home')


@login_required
def downvote(request, tip_id):
    """
    Ex05 : Downvote restreint par permission personnalisée 'tips.can_downvote'.
    Exception : l'auteur du tip peut toujours downvoter le sien.
    """
    tip = get_object_or_404(Tip, id=tip_id)
    user = request.user
    if tip.auteur != user and not user.has_perm('tips.can_downvote'):
        return redirect('home')
    if user in tip.downvoters.all():
        tip.downvoters.remove(user)
    else:
        tip.upvoters.remove(user)
        tip.downvoters.add(user)
    return redirect('home')


@login_required
def delete_tip(request, tip_id):
    """Ex04 : Auteur OU permission 'tips.delete_tip'."""
    tip = get_object_or_404(Tip, id=tip_id)
    user = request.user
    if tip.auteur == user or user.has_perm('tips.delete_tip'):
        tip.delete()
    return redirect('home')
