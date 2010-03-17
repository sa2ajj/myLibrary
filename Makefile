
all:

reset:
	python manage.py reset --noinput catalogue
	python manage.py syncdb

shell:
	python manage.py shell
