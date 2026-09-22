# Bookstore DRF

Projeto Django separado para o exercicio de Django REST Framework.

## Como executar

```powershell
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
```

## Como executar com Docker

```powershell
docker build -t bookstore-drf .
docker run --rm -p 8000:8000 bookstore-drf
```

Depois acesse:

```text
http://localhost:8000/
http://localhost:8000/api/books/
```

## Como executar com Docker Compose e Postgres

```powershell
docker compose up --build
```

O Docker Compose sobe dois servicos:

- `web`: aplicacao Django REST Framework
- `db`: banco PostgreSQL

Depois acesse:

```text
http://localhost:8000/
```

## Rotas

```text
/
/api/books/
/api-token-auth/
```

Para acessar `/api/orders/`, envie o token no header:

```text
Authorization: Token seu_token
```

## Testes

```powershell
poetry run pytest
```
