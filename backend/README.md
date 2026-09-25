# Backend

Django REST API for the AI Business Automation Dashboard.

## API

- GET /api/dashboard/
- GET /api/workflows/
- POST /api/workflows/
- GET /api/activity/

## Local setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Set database and secret values through environment variables.