# Bookstore DRF

Projeto Django separado para o exercicio de Django REST Framework.

## Como executar

```powershell
poetry install
poetry run python manage.py migrate
poetry run python manage.py runserver
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
