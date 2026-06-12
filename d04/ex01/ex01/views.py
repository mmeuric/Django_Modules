from django.shortcuts import render


def django_view(request):
    return render(request, 'ex01/django.html')


def affichage_view(request):
    return render(request, 'ex01/affichage.html')


def templates_view(request):
    return render(request, 'ex01/templates.html')
