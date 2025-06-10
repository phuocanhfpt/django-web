web: gunicorn ecommerce.wsgi --log-file -
web: bash -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn ecommerce.wsgi --log-file -"