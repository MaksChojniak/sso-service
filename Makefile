DEV  = docker compose -f docker-compose.yml -f docker-compose.dev.yml
PROD = docker compose -f docker-compose.yml -f docker-compose.prod.yml

proxy-network:
	docker network inspect proxy >/dev/null 2>&1 || docker network create proxy


# DEV
dev-up: proxy-network
	$(DEV) up -d --build

dev-reload: proxy-network
	$(DEV) up -d --build --force-recreate

dev-down:
	$(DEV) down

dev-logs-backend:
	$(DEV) logs -f backend
dev-logs-frontend:
	$(DEV) logs -f frontend
dev-migrate:
	$(DEV) exec backend python manage.py migrate


# PROD
prod:
	$(PROD) up -d --build

prod-down:
	$(PROD) down