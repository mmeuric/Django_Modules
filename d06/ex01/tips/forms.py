from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.Form):
    """Ex01 : 3 champs : username, password, password_confirm."""
    username = forms.CharField(
        max_length=150, label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )
    password_confirm = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'})
    )

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
    """Ex01 : 2 champs : username, password."""
    username = forms.CharField(
        max_length=150, label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"})
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'})
    )
