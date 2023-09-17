# Store Server

The project for study Django.

#### Stack:

- [Python](https://www.python.org/downloads/)
- [Django](https://www.djangoproject.com)
- [Django Rest Framework](https://www.django-rest-framework.org)
- [Docker Compose](https://www.docker.com)
- [PostgreSQL](https://www.postgresql.org/)
- [Celery](https://docs.celeryproject.org/en/stable/)
- [Redis](https://redis.io/)

## Local Developing

All actions should be executed from the source directory of the project and only after installing all requirements.

1. Firstly, create and activate a new virtual environment:
   ```bash
   poetry init
   ```
   
2. Install packages:
   ```bash
   poetry install
   ```
   
3. Run project dependencies, migrations, fill the database with the fixture data etc.:
   ```bash
   poetry run ./manage.py migrate
   poetry run ./manage.py loaddata .\products\fixtures\categories.json
   poetry run ./manage.py loaddata .\products\fixtures\goods.json
   poetry run ./manage.py runserver 
   ```
   
4. Run Docker:
   ```bash
   docker compose up -d
   ```
   
5. Run Celery:
   ```bash
   celery -A Store worker --loglevel=INFO
   ```

6. Run Django server:
   ```bash
   poetry run python ./manage.py runserver
   ```