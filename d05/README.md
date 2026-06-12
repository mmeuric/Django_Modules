# Formation Python-Django - Jour 05 : ORM

## Prérequis

```bash
pip install django psycopg2-binary
```

## Configuration PostgreSQL

```sql
CREATE DATABASE formationdjango;
CREATE ROLE djangouser WITH PASSWORD 'secret';
GRANT ALL PRIVILEGES ON DATABASE formationdjango TO djangouser;
ALTER ROLE djangouser CREATEDB;
```

## Lancer le serveur

```bash
python manage.py runserver
```

## Migrations (exercices ORM uniquement)

```bash
# Exercice 01
python manage.py makemigrations ex01
python manage.py migrate ex01

# Exercice 03
python manage.py makemigrations ex03
python manage.py migrate ex03

# Exercice 05
python manage.py makemigrations ex05
python manage.py migrate ex05

# Exercice 07
python manage.py makemigrations ex07
python manage.py migrate ex07

# Exercice 09
python manage.py makemigrations ex09
python manage.py migrate ex09
python manage.py loaddata ex09/ex09_initial_data.json

# Exercice 10
python manage.py makemigrations ex10
python manage.py migrate ex10
python manage.py loaddata ex10/ex10_initial_data.json
```

## URLs disponibles

| Exercice | URL | Description |
|---|---|---|
| ex00 | `/ex00/init` | Crée la table SQL ex00_movies |
| ex02 | `/ex02/init` | Crée la table SQL ex02_movies |
| ex02 | `/ex02/populate` | Insère les films Star Wars |
| ex02 | `/ex02/display` | Affiche les données |
| ex03 | `/ex03/populate` | Insère via ORM |
| ex03 | `/ex03/display` | Affiche via ORM |
| ex04 | `/ex04/init` | Crée la table SQL ex04_movies |
| ex04 | `/ex04/populate` | Insère (idempotent) |
| ex04 | `/ex04/display` | Affiche |
| ex04 | `/ex04/remove` | Supprime un film (formulaire) |
| ex05 | `/ex05/populate` | Insère via ORM (idempotent) |
| ex05 | `/ex05/display` | Affiche via ORM |
| ex05 | `/ex05/remove` | Supprime un film via ORM |
| ex06 | `/ex06/init` | Crée la table avec trigger PostgreSQL |
| ex06 | `/ex06/populate` | Insère |
| ex06 | `/ex06/display` | Affiche |
| ex06 | `/ex06/update` | Met à jour opening_crawl |
| ex07 | `/ex07/populate` | Insère via ORM |
| ex07 | `/ex07/display` | Affiche via ORM |
| ex07 | `/ex07/update` | Met à jour opening_crawl via ORM |
| ex08 | `/ex08/init` | Crée les tables planets & people |
| ex08 | `/ex08/populate` | Charge les CSV |
| ex08 | `/ex08/display` | Affiche les persos avec climat windy |
| ex09 | `/ex09/display` | Affiche via ORM (foreign key) |
| ex10 | `/ex10` | Formulaire de recherche Many-to-Many |
