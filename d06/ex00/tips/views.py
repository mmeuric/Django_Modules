import random
import time
from django.conf import settings
from django.shortcuts import render


def get_or_refresh_anon_name(request):
    """
    Ex00 : Attribue un nom anonyme aléatoire valable 42 secondes.
    Le nom est recalculé AVANT le rendu de la page pour être immédiatement visible.
    """
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
