from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    """
    Ex06 : Modèle utilisateur personnalisé avec système de réputation.

    Réputation calculée dynamiquement :
      - +5 pts par upvote reçu sur ses tips
      - -2 pts par downvote reçu sur ses tips
      - Tip supprimé => ses votes n'influencent plus la réputation

    Permissions débloquées automatiquement selon la réputation :
      - >= 15 pts : can_downvote (tips des autres)
      - >= 30 pts : delete_tip  (tips des autres)

    Si la réputation baisse sous le seuil, la permission est perdue.
    """

    @property
    def reputation(self):
        score = 0
        for tip in self.tips.all():
            score += tip.upvoters.count() * 5
            score -= tip.downvoters.count() * 2
        return score

    def has_perm(self, perm, obj=None):
        # Superuser bypass
        if self.is_active and self.is_superuser:
            return True
        rep = self.reputation
        # Déblocage automatique à 15 pts
        if perm == 'tips.can_downvote' and rep >= 15:
            return True
        # Déblocage automatique à 30 pts
        if perm == 'tips.delete_tip' and rep >= 30:
            return True
        return super().has_perm(perm, obj)

    def __str__(self):
        return self.username


class Tip(models.Model):
    contenu    = models.TextField()
    auteur     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tips')
    date       = models.DateTimeField(auto_now_add=True)
    upvoters   = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='upvoted_tips')
    downvoters = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='downvoted_tips')

    @property
    def upvote_count(self):
        return self.upvoters.count()

    @property
    def downvote_count(self):
        return self.downvoters.count()

    def __str__(self):
        return f"{self.auteur} — {self.contenu[:50]}"

    class Meta:
        ordering = ['-date']
        permissions = [
            ('can_downvote', 'Peut downvoter des Tips'),
        ]
