# Deploy no Heroku

Este projeto ja esta preparado para deploy no Heroku usando Poetry.

## Arquivos de deploy

- `Procfile`: declara o processo web com Gunicorn e a fase de release com migrations.
- `.python-version`: fixa a versao major do Python usada no Heroku.
- `.env.example`: lista as variaveis de ambiente esperadas.
- `docs/heroku-deploy-workflow.example.yml`: exemplo de workflow manual para deploy via GitHub Actions.

## Config Vars no Heroku

Configure no Heroku:

```text
SECRET_KEY=sua-chave-secreta
DEBUG=False
ALLOWED_HOSTS=nome-do-app.herokuapp.com,.herokuapp.com
CSRF_TRUSTED_ORIGINS=https://nome-do-app.herokuapp.com
```

Se voce anexar o add-on Heroku Postgres, o Heroku cria `DATABASE_URL` automaticamente.

## Deploy manual pelo Heroku Git

```powershell
heroku login
heroku create nome-do-app
heroku addons:create heroku-postgresql:essential-0 --app nome-do-app
heroku config:set SECRET_KEY="sua-chave-secreta" DEBUG=False ALLOWED_HOSTS="nome-do-app.herokuapp.com,.herokuapp.com" CSRF_TRUSTED_ORIGINS="https://nome-do-app.herokuapp.com" --app nome-do-app
git push heroku main
```

## Deploy pelo GitHub Actions

Para usar o exemplo de workflow, copie `docs/heroku-deploy-workflow.example.yml` para `.github/workflows/heroku-deploy.yml` e configure estes secrets no GitHub:

```text
HEROKU_API_KEY
HEROKU_APP_NAME
```

O exemplo usa `workflow_dispatch`, entao o deploy e iniciado manualmente pela aba Actions do GitHub.
