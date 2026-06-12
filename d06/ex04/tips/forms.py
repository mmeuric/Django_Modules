from django import forms
from django.contrib.auth import get_user_model
from .models import Tip

User = get_user_model()


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned = super().clean()
        username = cleaned.get('username')
        pw = cleaned.get('password')
        pw2 = cleaned.get('password_confirm')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        if pw and pw2 and pw != pw2:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class TipForm(forms.ModelForm):
    """Ex02 : ModelForm pour créer un Tip."""
    class Meta:
        model = Tip
        fields = ['contenu']
        widgets = {'contenu': forms.Textarea(attrs={
            'class': 'form-control', 'rows': 3,
            'placeholder': 'Votre Life Pro Tip...'
        })}
        labels = {'contenu': ''}
