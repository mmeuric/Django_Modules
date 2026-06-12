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
            CREATE TABLE IF NOT EXISTS ex00_movies (
                episode_nb    INTEGER PRIMARY KEY,
                title         VARCHAR(64) UNIQUE NOT NULL,
                opening_crawl TEXT,
                director      VARCHAR(32) NOT NULL,
                producer      VARCHAR(128) NOT NULL,
                release_date  DATE NOT NULL
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
