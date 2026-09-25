# AI Business Automation Dashboard

> **SSVPrasad portfolio project** demonstrating an AI-assisted workflow automation platform.

This project is designed around a simple automation loop:

**Business problem → workflow design → trigger → ordered actions → execution → output → observability**

It serves two purposes:
1. **Portfolio proof:** demonstrate practical AI automation, backend/API, workflow architecture and observability skills.
2. **Freelance foundation:** provide reusable architecture that can later be adapted to a real client's approved integrations and business processes.

No real client, customer, revenue, productivity or business-result claims are represented.

## Current Product Structure

### 1. AI Workflow Builder
A user describes a repetitive business process. The backend can use OpenAI to propose:
- workflow name
- trigger
- action steps
- expected value

The proposal can be saved as a workflow.

### 2. Workflow Management
Each workflow contains:
- trigger definition
- status
- ordered action steps
- run count
- success rate

Supported action types currently include:
- AI Process
- Transform
- Webhook
- Email
- Log

The action types provide the architecture for integrations; external side effects are not automatically enabled by the public demo.

### 3. Execution Engine
An active workflow can be started with **Run now**.

The execution layer:
- creates an execution record
- processes the configured steps
- records step-level activity
- records final status/output
- updates workflow analytics

This is the internal execution framework. External actions such as sending a real email or modifying a CRM require a separately configured integration.

### 4. Live Automation Demo
The dashboard contains a sandboxed **AI Lead Qualification** demo.

Visitor flow:

```
Customer enquiry
      ↓
Receive input
      ↓
AI / sandbox qualification
      ↓
Classify priority
      ↓
Generate suggested response
      ↓
Display result
```

The public demo does not send email, access a real CRM, or perform arbitrary external actions.

When `OPENAI_API_KEY` is configured, the demo attempts an AI-powered result. Without it, a deterministic sandbox result is returned so the workflow can still be demonstrated safely.

### 5. Execution History
The Activity and execution views expose:
- workflow
- execution status
- individual step events
- timestamps
- output/error information

## Architecture

```
React + Vite
    │
    ├── Dashboard
    ├── AI Workflow Builder
    ├── Automation Builder
    ├── Live Demo
    ├── Activity
    └── Integration layer
    │
    ▼
Django REST Framework
    │
    ├── Workflow API
    ├── Workflow Step API
    ├── Execution API
    ├── Activity API
    ├── AI Suggestion API
    └── Live Demo API
    │
    ▼
PostgreSQL
    │
    ├── Workflows
    ├── Workflow Steps
    ├── Executions
    └── Activity Events

AI provider
    │
    └── OpenAI workflow intelligence / demo analysis
```

## API

- `GET /api/dashboard/`
- `GET /api/workflows/`
- `POST /api/workflows/`
- `POST /api/workflows/{id}/run/`
- `GET /api/steps/`
- `POST /api/steps/`
- `GET /api/executions/`
- `GET /api/activity/`
- `POST /api/ai/suggest/`
- `POST /api/demo/lead/`

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

Copy the environment examples to local environment files. Keep secrets out of Git.

## Environment

Backend:
- `DJANGO_SECRET_KEY`
- `DATABASE_URL`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`

Frontend:
- `VITE_API_BASE_URL`

## From Portfolio to Freelance

The repository is intentionally structured so a future client solution can be built from the same core:

```
Client business problem
        ↓
Discovery / requirements
        ↓
Workflow configuration
        ↓
Authorized integration
        ↓
Trigger
        ↓
Actions
        ↓
Execution + retries
        ↓
Logs + monitoring
        ↓
Client-specific output
```

For a real client deployment, integrations, authentication, authorization, secrets, rate limits, retries, queues/workers and audit requirements should be configured according to the client's environment.

## Developer

**SSVPrasad** — Full-Stack Developer · AI Integration · Backend · 3D Web

Portfolio: https://ssvprasad144.github.io/3d-motion-portfolio/
