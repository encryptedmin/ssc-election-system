# SSC Election System

Django-based student council election system prepared for a Render proof-of-concept deployment.

## Render deployment

This repo includes a `render.yaml` blueprint. On Render, create a new Blueprint instance from this repository and Render will use:

- Build command: `bash build.sh`
- Start command: `python -m gunicorn config.wsgi:application`
- Python version: `.python-version`

The committed `db.sqlite3` and `media/` files are intentionally included so the deployed app starts with the existing demo/test data. Render web services use an ephemeral filesystem by default, so runtime changes to this SQLite database are suitable for demos only and can be reset by redeploys. For production, migrate to Render Postgres.

## Local setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
