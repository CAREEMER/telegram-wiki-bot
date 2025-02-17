## Commands

### Export project requirements
`poetry export -f requirements.txt --output src/requirements.txt`

### Generate migrations
`alembic revision --autogenerate -m "init"`
`alembic upgrade head`

### Purge pending tasks
`celery -A celery_app purge`

### Pg dump
`pg_dump -h localhost -p 5432 -U sample_tg_bot_app -d sample_tg_bot_app > dump.sql`

### Pg restore
`docker exec -i capstrade-bot-db-1 psql -U sample_tg_bot_app -d sample_tg_bot_app < dump.sql`
`or if using pg_restore`
`docker exec -i capstrade-bot-db-1 pg_restore -U sample_tg_bot_app -d sample_tg_bot_app < dump.sql`
