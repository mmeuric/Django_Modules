from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Tip


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Ex04 : Interface admin pour gérer les permissions manuellement.
    Accorder 'tips | tip | Can delete tip' à un utilisateur pour tester.
    """
    pass


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'contenu_court', 'date')

    def contenu_court(self, obj):
        return obj.contenu[:60]
    contenu_court.short_description = 'Contenu'
