# Kafka Chat

## Feautures
* Microservice Architecture (Auth, Users, Chat, Notifications)
* Kafka Message Broker
* NGINX API Gateway
* JWT Token Auth (self-verification of the token using the  public key for each microservice)
* User confirmation by email

## How to run
* Generate private and public key via RS256 algorithm, set auth environment variables `./services/auth/.env.production`
    
    ```python
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_DB=kafkachat

    KAFKA_URL=kafka:29092

    PRIVATE_KEY=
    PUBLIC_KEY=
    ```
    Set users environment variables `./services/users/.env.production`
    ```python
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_DB=kafkachat
    ```
    Set notifications environment variables `./services/notifications/.env.production`
    ```python
    SMTP_PASSWORD=
    SMTP_HOST=
    SMTP_PORT=
    SMTP_EMAIL=
    SMTP_SUBJECT=

    KAFKA_URL=kafka:29092
    ```
    ### Development
    * Run `make app` or `docker compose up -d` in the project directory
    ### Production
    * Run `make prod` or `docker compose -f docker-compose.production.yml up -d` in the project directory

## Architecture
![architecture](./docs/images/architecture.png)