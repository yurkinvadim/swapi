sort:
	isort .

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

requirements:
	pip freeze > requirements.txt

run:
	python manage.py runserver

su:
	python manage.py createsuperuser

test:
	pytest

tests:
	pytest

shell:
	python manage.py shell