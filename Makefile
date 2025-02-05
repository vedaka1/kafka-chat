DC = docker compose
PROD = ./docker-compose.production.yml

certs:
	openssl req -new -newkey rsa:4096 -x509 -sha256 -days 365 -nodes -out ./nginx/nginx-certificate.crt -keyout ./nginx/nginx.key
app:
	$(DC) up -d --build

app-down: 
	$(DC) down

prod:
	$(DC) -f $(PROD) up -d --build
 
prod-down:
	$(DC) -f $(PROD) down

.PHONY: app app-down prod prod-down certs