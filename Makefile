install:
	poetry install

install-prod:
	poetry install --no-dev

lint:
	poetry run flake8 task_manager

pylint:
	poetry run pylint task_manager

test:
	poetry run python manage.py test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py,*/migrations/*,*/tests/*,tests.py

messages:
	poetry run python manage.py makemessages -l ru
	msgattrib --clear-fuzzy task_manager/locale/ru/LC_MESSAGES/django.po -o task_manager/locale/ru/LC_MESSAGES/django.po
	poetry run python manage.py makemessages -l en
	msgattrib --clear-fuzzy task_manager/locale/en/LC_MESSAGES/django.po -o task_manager/locale/en/LC_MESSAGES/django.po

compile-messages:
	poetry run python manage.py compilemessages

shell:
	poetry run python manage.py shell_plus

static:
	poetry run python manage.py collectstatic

createsuperuser:
	poetry run python manage.py createsuperuser --noinput

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

dev: migrate
	DEBUG=True poetry run python manage.py runserver

build:
	./build.sh

PORT := 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

.PHONY: install install-prod lint pylint test test-coverage messages compile-messages shell static createsuperuser migrate dev build start
