DC = docker compose
PROD = ./docker-compose.production.yml


app:
	$(DC) up -d --build

app-down: 
	$(DC) down

prod:
	$(DC) -f $(PROD) up -d --build
 
prod-down:
	$(DC) -f $(PROD) down

.PHONY: app app-down prod prod-down