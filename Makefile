install:
	poetry install

lint:
	poetry run flake8 task_manager

pylint:
	poetry run pylint task_manager

test:
	poetry run python manage.py test

messages-ru:
	poetry run django-admin makemessages -l ru

messages-en:
	poetry run django-admin makemessages -l en

compile-messages:
	poetry run django-admin compilemessages

shell:
	poetry run python manage.py shell_plus

static: install
	poetry run python manage.py collectstatic

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

dev: migrate
	poetry run python manage.py runserver

build:
	./build.sh

PORT := 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

.PHONY: install lint pylint messages-ru messages-en compile-messages shell static migrate dev build start
