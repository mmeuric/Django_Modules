from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Tip


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Ex06 : Admin avec affichage de la réputation.
    Les permissions sont désormais gérées automatiquement par la réputation.
    On peut toujours les accorder manuellement via l'admin pour tests.
    """
    list_display = ('username', 'email', 'is_staff', 'reputation_display')
    readonly_fields = ('reputation_display',)

    def reputation_display(self, obj):
        return f"{obj.reputation} pts"
    reputation_display.short_description = 'Réputation'


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'contenu_court', 'date', 'upvote_count', 'downvote_count')

    def contenu_court(self, obj):
        return obj.contenu[:60]
    contenu_court.short_description = 'Contenu'
