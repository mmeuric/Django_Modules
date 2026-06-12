from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Movies

MOVIES_DATA = [
    {'episode_nb': 1, 'title': 'The Phantom Menace',      'director': 'George Lucas',     'producer': 'Rick McCallum',                                      'release_date': '1999-05-19'},
    {'episode_nb': 2, 'title': 'Attack of the Clones',    'director': 'George Lucas',     'producer': 'Rick McCallum',                                      'release_date': '2002-05-16'},
    {'episode_nb': 3, 'title': 'Revenge of the Sith',     'director': 'George Lucas',     'producer': 'Rick McCallum',                                      'release_date': '2005-05-19'},
    {'episode_nb': 4, 'title': 'A New Hope',               'director': 'George Lucas',     'producer': 'Gary Kurtz, Rick McCallum',                          'release_date': '1977-05-25'},
    {'episode_nb': 5, 'title': 'The Empire Strikes Back',  'director': 'Irvin Kershner',   'producer': 'Gary Kutz, Rick McCallum',                           'release_date': '1980-05-17'},
    {'episode_nb': 6, 'title': 'Return of the Jedi',       'director': 'Richard Marquand', 'producer': 'Howard G. Kazanjian, George Lucas, Rick McCallum',   'release_date': '1983-05-25'},
    {'episode_nb': 7, 'title': 'The Force Awakens',        'director': 'J. J. Abrams',     'producer': 'Kathleen Kennedy, J. J. Abrams, Bryan Burk',         'release_date': '2015-12-11'},
]


def populate(request):
    results = []
    for data in MOVIES_DATA:
        try:
            _, created = Movies.objects.get_or_create(
                episode_nb=data['episode_nb'],
                defaults=data
            )
            results.append("OK")
        except Exception as e:
            results.append(str(e))
    return HttpResponse("<br>".join(results))


def display(request):
    try:
        movies = Movies.objects.all().order_by('episode_nb')
        if not movies.exists():
            return HttpResponse("No data available")
        fields = ['episode_nb', 'title', 'opening_crawl', 'director', 'producer', 'release_date', 'created', 'updated']
        html = "<table border='1'><tr>" + "".join(f"<th>{f}</th>" for f in fields) + "</tr>"
        for m in movies:
            html += "<tr>" + "".join(f"<td>{getattr(m, f)}</td>" for f in fields) + "</tr>"
        html += "</table>"
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse("No data available")


@csrf_exempt
def update(request):
    try:
        if request.method == 'POST':
            title = request.POST.get('title')
            crawl = request.POST.get('opening_crawl', '')
            if title:
                Movies.objects.filter(title=title).update(opening_crawl=crawl)
        movies = Movies.objects.all().order_by('title')
        if not movies.exists():
            return HttpResponse("No data available")
        options = "".join(f"<option value='{m.title}'>{m.title}</option>" for m in movies)
        html = f"""<form method="post">
            <label>Film: <select name="title">{options}</select></label><br><br>
            <label>Opening crawl:<br>
            <textarea name="opening_crawl" rows="5" cols="60"></textarea></label><br><br>
            <input type="submit" value="update">
        </form>"""
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse("No data available")
