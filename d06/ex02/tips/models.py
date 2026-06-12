from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    def __str__(self):
        return self.username


class Tip(models.Model):
    """
    Ex02 : Modèle Tip avec contenu, auteur, date.
    """
    contenu = models.TextField()
    auteur  = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tips'
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.auteur} — {self.contenu[:50]}"

    class Meta:
        ordering = ['-date']
