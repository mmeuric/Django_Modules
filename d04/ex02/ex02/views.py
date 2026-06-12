import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import timezone
from .forms import EntryForm


def index(request):
    form = EntryForm()
    history = []

    log_path = settings.LOG_FILE

    # Lire l'historique existant depuis le fichier de logs
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    history.append(line)

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry_text = form.cleaned_data['entry']
            timestamp = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            log_entry = f'[{timestamp}] {entry_text}'

            # Écrire dans le fichier de logs (créé automatiquement s'il n'existe pas)
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(log_entry + '\n')

            # Redirection POST → GET pour éviter la re-soumission
            return redirect('/ex02/')

    return render(request, 'ex02/index.html', {
        'form': form,
        'history': history,
    })
