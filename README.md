# AI Business Automation Dashboard

> Portfolio project by **SSVPrasad** demonstrating a client-style AI automation platform.

A full-stack business automation dashboard for designing, monitoring, and extending AI-assisted business workflows.

## Architecture

```
React + Vite → Django REST Framework → PostgreSQL
                         │
                         └── OpenAI workflow suggestions
```

## Implemented

- Responsive React dashboard
- Workflow management UI
- Django REST API
- PostgreSQL-ready models and migrations
- Dashboard aggregation endpoint
- Activity API
- OpenAI workflow suggestion service
- Environment-based configuration
- Django admin
- Production-ready backend dependencies

## API

- `GET /api/dashboard/`
- `GET /api/workflows/`
- `POST /api/workflows/`
- `GET /api/activity/`
- `POST /api/ai/suggest/`

## Local Development

### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Copy `.env.example` to `.env`. Keep real API keys out of Git.

## AI Workflow Suggestion

`POST /api/ai/suggest/` accepts a business-process description and, when `OPENAI_API_KEY` is configured, returns an AI-generated workflow proposal.

This is a portfolio implementation; no real client results or customer claims are represented.

## Developer

**SSVPrasad** — Full-Stack Developer · AI Integration · Backend · 3D Web

Portfolio: https://ssvprasad144.github.io/3d-motion-portfolio/
