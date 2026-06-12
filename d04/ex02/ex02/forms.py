from django import forms


class EntryForm(forms.Form):
    entry = forms.CharField(
        label='Votre texte',
        max_length=500,
        widget=forms.TextInput(attrs={
            'placeholder': 'Saisissez votre texte ici...',
            'style': 'width: 400px; padding: 6px;',
        })
    )
