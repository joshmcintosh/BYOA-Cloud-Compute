python ccf/manage.py makemigrations
python ccf/manage.py migrate
python ccf/manage.py collectstatic --noinput
python ccf/manage.py runserver "0.0.0.0:$PORT" --noreload
