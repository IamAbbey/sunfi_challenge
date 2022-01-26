## Project: Sunfi Challenge

### Setup
- To begin, clone this repository `git clone `
- Without Docker
  - Run makemigrations with `python manage.py makemigration`
  - Run migrations with `python manage.py migrate`
  - Start local server with `python manage.py runserver`
  - Open browser and go to `http://127.0.0.1:8000/`
- With Docker
  - To begin, run `docker-compose up --build -d`
  - Run migrations with `docker-compose exec api python manage.py migrate`
  - Run test with `docker-compose exec api coverage run -m pytest`
  - Generate html report with `docker-compose exec api coverage html`
  - Open browser and go to http://127.0.0.1:8000/


### MVP test coverage: 100%
- Run the tests with coverage:
```sh
$ coverage run -m pytest
$ coverage html
$ open htmlcov/index.html

### Lint Check
```sh
$ flake8 .
$ black .
$ isort .
```

### Feature List
- A new user can be signup

- Users of the system can sigin with their email and password

- An Authorization token is generated on successful login -  which is to be added as an Authorization header to requests that need authentication

- Signed in user can:
    - Get list of characters
    - Get list of character's quote
    - Get character's quote details
    - Get character's details
    - Get list of users
    - Favorite a character
    - Favorite a character's quote
  
Mentions
=======

This project was given a development head start with some of my packages
DRF Compose (<https://github.com/IamAbbey/drf_compose>) and
py-sync-dotenv (<https://github.com/IamAbbeypy_sync_dotenv>) to seemlessly synchronizing .env files across the projects.
