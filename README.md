# filmography_app

## Description

An application that connects with outer API that allows searching filmography of selected actors.

## Prerequisites and usage


- git clone
- cd filmography_app
- pip install -r requirements.txt
- set enviroment variable - API_KEY (from RAPIDAPI.com)
- cd my_app
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver

## For testing

- need to set enviroment variable: DJANGO_APP_STAGE=testing

## Technologies

- Python
- Django

## To do:

- Possibility to save favorite actors and get a newsletter about new movies which they appeared.
- Apply APScheduler module to schedule tasks on production environment (deployed on Heroku).
