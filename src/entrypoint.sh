#!/bin/sh

echo "waiting for postgres..."

while  ! nc -z $DATABASE_HOST 5432; do
    sleep 0.1
done

echo "postgres started"

alembic upgrade head

exec "$@"
