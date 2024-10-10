install:
	poetry install

lint:
	poetry run flake8 task_manager

pylint:
	poetry run pylint task_manager

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

dev: migrate
	poetry run python manage.py runserver

build:
	./build.sh

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

PHONY: install lint pylint migrate dev build start
