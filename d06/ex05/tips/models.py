from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
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
            # Ex05 : permission personnalisée pour restreindre le downvote
            ('can_downvote', 'Peut downvoter des Tips'),
        ]
