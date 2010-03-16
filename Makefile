
all:

reset:
	python manage.py reset --noinput catalogue
	python manage.py syncdb
