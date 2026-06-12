from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Movies, People


@csrf_exempt
def index(request):
    try:
        genders = (
            People.objects
            .values_list('gender', flat=True)
            .distinct()
            .exclude(gender__isnull=True)
            .exclude(gender='')
            .order_by('gender')
        )

        results = None
        searched = False
        error_msg = ''

        if request.method == 'POST':
            searched = True
            min_date = request.POST.get('min_date', '')
            max_date = request.POST.get('max_date', '')
            min_diam = request.POST.get('min_diameter', '')
            gender   = request.POST.get('gender', '')

            if not all([min_date, max_date, min_diam, gender]):
                error_msg = 'All fields are required.'
            else:
                try:
                    results = Movies.objects.filter(
                        release_date__gte=min_date,
                        release_date__lte=max_date,
                        characters__gender=gender,
                        characters__homeworld__diameter__gte=int(min_diam),
                    ).values(
                        'title',
                        'characters__name',
                        'characters__gender',
                        'characters__homeworld__name',
                        'characters__homeworld__diameter',
                    ).order_by('title', 'characters__name')
                except Exception as e:
                    results = []
                    error_msg = str(e)

        gender_options = "".join(
            f"<option value='{g}'>{g}</option>" for g in genders
        )

        html = f"""<!DOCTYPE html>
<html>
<head><title>Ex10 - Many to Many</title></head>
<body>
<h2>Search Characters in Movies</h2>
<form method="post">
    <table>
        <tr>
            <td><label>Movies minimum release date:</label></td>
            <td><input type="date" name="min_date" required></td>
        </tr>
        <tr>
            <td><label>Movies maximum release date:</label></td>
            <td><input type="date" name="max_date" required></td>
        </tr>
        <tr>
            <td><label>Planet diameter greater than:</label></td>
            <td><input type="number" name="min_diameter" required></td>
        </tr>
        <tr>
            <td><label>Character gender:</label></td>
            <td><select name="gender">{gender_options}</select></td>
        </tr>
        <tr>
            <td colspan="2"><input type="submit" value="Search"></td>
        </tr>
    </table>
</form>
"""
        if error_msg:
            html += f"<p style='color:red'>{error_msg}</p>"

        if searched and results is not None:
            if not results:
                html += "<p>Nothing corresponding to your research</p>"
            else:
                html += """<table border='1'>
                    <tr>
                        <th>Movie</th>
                        <th>Character</th>
                        <th>Gender</th>
                        <th>Homeworld</th>
                        <th>Diameter</th>
                    </tr>"""
                for r in results:
                    html += (
                        f"<tr>"
                        f"<td>{r['title']}</td>"
                        f"<td>{r['characters__name']}</td>"
                        f"<td>{r['characters__gender']}</td>"
                        f"<td>{r['characters__homeworld__name']}</td>"
                        f"<td>{r['characters__homeworld__diameter']}</td>"
                        f"</tr>"
                    )
                html += "</table>"

        html += "</body></html>"
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"Error: {e}")
