import io
import os
import psycopg2
from django.http import HttpResponse

DB_SETTINGS = {
    'dbname': 'formationdjango',
    'user': 'djangouser',
    'password': 'secret',
    'host': 'localhost',
    'port': '5432',
}


def init(request):
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ex08_planets (
                id              SERIAL PRIMARY KEY,
                name            VARCHAR(64) UNIQUE NOT NULL,
                climate         VARCHAR,
                diameter        INTEGER,
                orbital_period  INTEGER,
                population      BIGINT,
                rotation_period INTEGER,
                surface_water   REAL,
                terrain         VARCHAR(128)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ex08_people (
                id          SERIAL PRIMARY KEY,
                name        VARCHAR(64) UNIQUE NOT NULL,
                birth_year  VARCHAR(32),
                gender      VARCHAR(32),
                eye_color   VARCHAR(32),
                hair_color  VARCHAR(32),
                height      INTEGER,
                mass        REAL,
                homeworld   VARCHAR(64) REFERENCES ex08_planets(name)
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def _parse_csv_to_stringio(filepath, null_val='N/A'):
    """Read a CSV file and replace null_val with \\N for psycopg2 copy_from."""
    lines = []
    with open(filepath, 'r', encoding='utf-8') as f:
        next(f)  # skip header
        for line in f:
            line = line.rstrip('\n')
            fields = line.split(',')
            fields = ['\\N' if v.strip() == null_val or v.strip() == '' else v for v in fields]
            lines.append('\t'.join(fields))
    return io.StringIO('\n'.join(lines))


def populate(request):
    results = []
    base_dir = os.path.dirname(__file__)
    files = [
        ('planets.csv', 'ex08_planets', ['name', 'climate', 'diameter', 'orbital_period', 'population', 'rotation_period', 'surface_water', 'terrain']),
        ('people.csv',  'ex08_people',  ['name', 'birth_year', 'gender', 'eye_color', 'hair_color', 'height', 'mass', 'homeworld']),
    ]
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cursor = conn.cursor()
        for filename, table, columns in files:
            try:
                filepath = os.path.join(base_dir, filename)
                buf = _parse_csv_to_stringio(filepath)
                cursor.copy_from(buf, table, sep='\t', null='\\N', columns=columns)
                conn.commit()
                results.append(f"{filename}: OK")
            except Exception as e:
                conn.rollback()
                results.append(f"{filename}: {e}")
        cursor.close()
        conn.close()
    except Exception as e:
        return HttpResponse(f"Connection error: {e}")
    return HttpResponse("<br>".join(results))


def display(request):
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.name, pl.name AS homeworld, pl.climate
            FROM ex08_people p
            JOIN ex08_planets pl ON p.homeworld = pl.name
            WHERE pl.climate LIKE '%windy%'
            ORDER BY p.name;
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        if not rows:
            return HttpResponse("No data available")
        html = "<table border='1'><tr><th>Name</th><th>Homeworld</th><th>Climate</th></tr>"
        for row in rows:
            html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        html += "</table>"
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse("No data available")
