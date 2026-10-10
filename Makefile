DEV  = docker compose -f docker-compose.yml -f docker-compose.dev.yml
PROD = docker compose -f docker-compose.yml -f docker-compose.prod.yml

dev:
	$(DEV) up --build

dev-down:
	$(DEV) down

prod:
	$(PROD) up -d --build

prod-down:
	$(PROD) down

migrate:
	$(DEV) exec backend python manage.py migrate