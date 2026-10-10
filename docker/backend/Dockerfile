FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ---- dev ----
FROM base AS dev
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ---- prod ----
FROM base AS prod
RUN useradd -m appuser && chown -R appuser /app
USER appuser
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]