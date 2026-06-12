from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Ex01 : Modèle utilisateur personnalisé (anticipation ex06).
    Permet de remplacer facilement le modèle par défaut plus tard.
    """
    pass

    def __str__(self):
        return self.username
