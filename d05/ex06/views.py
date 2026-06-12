import psycopg2
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

DB_SETTINGS = {
    'dbname': 'formationdjango',
    'user': 'djangouser',
    'password': 'secret',
    'host': 'localhost',
    'port': '5432',
}

MOVIES_DATA = [
    (1, 'The Phantom Menace',      'George Lucas',     'Rick McCallum',                                      '1999-05-19'),
    (2, 'Attack of the Clones',    'George Lucas',     'Rick McCallum',                                      '2002-05-16'),
    (3, 'Revenge of the Sith',     'George Lucas',     'Rick McCallum',                                      '2005-05-19'),
    (4, 'A New Hope',              'George Lucas',     'Gary Kurtz, Rick McCallum',                          '1977-05-25'),
    (5, 'The Empire Strikes Back', 'Irvin Kershner',   'Gary Kutz, Rick McCallum',                           '1980-05-17'),
    (6, 'Return of the Jedi',      'Richard Marquand', 'Howard G. Kazanjian, George Lucas, Rick McCallum',   '1983-05-25'),
    (7, 'The Force Awakens',       'J. J. Abrams',     'Kathleen Kennedy, J. J. Abrams, Bryan Burk',         '2015-12-11'),
]


def init(request):
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ex06_movies (
                episode_nb    INTEGER PRIMARY KEY,
                title         VARCHAR(64) UNIQUE NOT NULL,
                opening_crawl TEXT,
                director      VARCHAR(32) NOT NULL,
                producer      VARCHAR(128) NOT NULL,
                release_date  DATE NOT NULL,
                created       TIMESTAMP DEFAULT NOW(),
                updated       TIMESTAMP DEFAULT NOW()
            );
        """)
        cursor.execute("""
            CREATE OR REPLACE FUNCTION update_changetimestamp_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated = now();
                NEW.created = OLD.created;
                RETURN NEW;
            END;
            $$ language 'plpgsql';
        """)
        cursor.execute("""
            DROP TRIGGER IF EXISTS update_films_changetimestamp ON ex06_movies;
            CREATE TRIGGER update_films_changetimestamp
            BEFORE UPDATE ON ex06_movies
            FOR EACH ROW EXECUTE PROCEDURE update_changetimestamp_column();
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {e}")


def populate(request):
    results = []
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cursor = conn.cursor()
        for ep, title, director, producer, release_date in MOVIES_DATA:
            try:
                cursor.execute("""
                    INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (episode_nb) DO NOTHING
                """, (ep, title, director, producer, release_date))
                conn.commit()
                results.append("OK")
            except Exception as e:
                conn.rollback()
                results.append(f"{title}: {e}")
        cursor.close()
        conn.close()
    except Exception as e:
        return HttpResponse(f"Database connection error: {e}")
    return HttpResponse("<br>".join(results))


def display(request):
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ex06_movies ORDER BY episode_nb;")
        rows = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        if not rows:
            return HttpResponse("No data available")
        html = "<table border='1'><tr>" + "".join(f"<th>{c}</th>" for c in cols) + "</tr>"
        for row in rows:
            html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        html += "</table>"
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse("No data available")


@csrf_exempt
def update(request):
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cursor = conn.cursor()
        if request.method == 'POST':
            title = request.POST.get('title')
            crawl = request.POST.get('opening_crawl', '')
            if title:
                cursor.execute(
                    "UPDATE ex06_movies SET opening_crawl = %s WHERE title = %s",
                    (crawl, title)
                )
                conn.commit()
        cursor.execute("SELECT title FROM ex06_movies ORDER BY title;")
        titles = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        if not titles:
            return HttpResponse("No data available")
        options = "".join(f"<option value='{t}'>{t}</option>" for t in titles)
        html = f"""<form method="post">
            <label>Film: <select name="title">{options}</select></label><br><br>
            <label>Opening crawl:<br>
            <textarea name="opening_crawl" rows="5" cols="60"></textarea></label><br><br>
            <input type="submit" value="update">
        </form>"""
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse("No data available")
