from django.shortcuts import render


def index(request):
    rows = []
    for i in range(50):
        # Valeur allant de 0 (ligne 0 = foncé) à 255 (ligne 49 = clair)
        value = int(i * 255 / 49)
        row = [
            f'rgb({value},{value},{value})',  # Noir → blanc
            f'rgb({value},0,0)',              # Noir → rouge
            f'rgb(0,0,{value})',              # Noir → bleu
            f'rgb(0,{value},0)',              # Noir → vert
        ]
        rows.append(row)

    context = {
        'columns': ['Noir', 'Rouge', 'Bleu', 'Vert'],
        'rows': rows,
    }
    return render(request, 'ex03/index.html', context)
