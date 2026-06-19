# Deployment Guide

## Docker Deployment

1. Copy `backend/.env.example` to `backend/.env` and set secure production values.
2. From the repository root, run:

```bash
docker compose up --build -d
```

3. Verify services started successfully:

```bash
docker compose ps
```

4. The backend should be available at `http://localhost:8000`.
5. Use `docker compose logs -f backend` to monitor startup.

## Backend Local Development

From `backend/`:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
pytest
python -m pyright --outputjson
flake8 app
```

## Frontend Local Development

From `frontend/`:

```bash
npm install
npm run dev
```

Build for production:

```bash
npm install
npm run build
```

## Render Deployment

- `render.yaml` is included for Render deploys.
- Set `VITE_API_BASE_URL` to the deployed backend base URL.
- The frontend uses `VITE_API_BASE_URL` at build time, so `frontend/.env.example` should be updated before local environment builds.
- Build the frontend before deploying static assets if using a separate host.

## Environment Variables

- `APP_NAME`: Application name
- `APP_ENV`: `production` or `development`
- `TESTING`: `false` in production
- `SECRET_KEY`: strong JWT signing key
- `ALGORITHM`: JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: token lifetime
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis broker/cache URL
- `CORS_ORIGINS`: allowed origins list (avoid `*` in production unless you understand the consequences)
- `RATE_LIMIT_PER_MINUTE`: API rate limit
- `LOG_LEVEL`: application log level
- `SENTRY_DSN`: optional Sentry reporting
- `VITE_API_BASE_URL`: frontend API host for browser requests

## Running Tests

From `backend/`:

```bash
pytest
```

## Runtime Validation

- `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- `celery -A tasks.celery_app.celery_app worker -l info`
- `alembic upgrade head`

## Notes

- The backend exposes FastAPI docs at `/docs`.
- Security headers are added automatically in production.
- Rate limiting is enforced globally by IP.
- Sentry is enabled when `SENTRY_DSN` is configured.
