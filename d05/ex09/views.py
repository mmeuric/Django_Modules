from django.http import HttpResponse
from .models import People


def display(request):
    try:
        people = People.objects.filter(
            homeworld__climate__icontains='windy'
        ).select_related('homeworld').order_by('name')

        if not people.exists():
            return HttpResponse(
                "No data available, please use the following command line before use:<br>"
                "<code>python manage.py loaddata ex09_initial_data.json</code>"
            )

        html = "<table border='1'><tr><th>Name</th><th>Homeworld</th><th>Climate</th></tr>"
        for p in people:
            hw_name = p.homeworld.name if p.homeworld else 'N/A'
            hw_climate = p.homeworld.climate if p.homeworld else 'N/A'
            html += f"<tr><td>{p.name}</td><td>{hw_name}</td><td>{hw_climate}</td></tr>"
        html += "</table>"
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(
            "No data available, please use the following command line before use:<br>"
            "<code>python manage.py loaddata ex09_initial_data.json</code>"
        )
