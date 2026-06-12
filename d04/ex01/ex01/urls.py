from django.urls import path
from . import views

urlpatterns = [
    path('django', views.django_view, name='ex01_django'),
    path('affichage', views.affichage_view, name='ex01_affichage'),
    path('templates', views.templates_view, name='ex01_templates'),
]
