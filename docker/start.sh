#!/usr/bin/env sh
set -e

# Collect static
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Start nginx
nginx

# Start server
uwsgi --uid www-data \
    --gid www-data \
    --socket /tmp/uwsgi.sock \
    --module kees.wsgi \
    --processes 4 \
    --threads 2
