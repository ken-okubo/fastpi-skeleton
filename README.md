# FastAPI Skeleton

Template base para projetos FastAPI com Docker, PostgreSQL, Alembic e JWT auth.

Base template for FastAPI projects with Docker, PostgreSQL, Alembic and JWT auth.

---

## O que vem incluso / What's included

- **FastAPI** com CORS, health check e Swagger UI (`/docs`)
- **PostgreSQL 15** via Docker Compose
- **SQLAlchemy 2.0** + **Alembic** para migrations
- **JWT Auth** com access/refresh tokens e RBAC (roles: user, admin)
- **Rotas prontas / Ready-made routes**: register, login, refresh, me, change-password
- **Script `create_admin.py`** para criar o primeiro admin / to create the first admin user
- **Dual-mode Docker**: local (wait-for-postgres) e Railway/production (start.sh)

## Estrutura / Structure

```
├── app/
│   ├── core/
│   │   ├── config.py       # Settings via .env (pydantic-settings)
│   │   ├── db.py           # Engine, session, get_db
│   │   └── security.py     # JWT, get_current_user, RBAC
│   ├── models/
│   │   └── user.py         # User + UserRole (UUID PK)
│   ├── schemas/
│   │   ├── base.py         # DateTimeUTC serializer
│   │   ├── auth.py         # Token, LoginRequest, etc.
│   │   └── user.py         # UserCreate, UserResponse
│   ├── crud/
│   │   └── user.py         # create, authenticate, etc.
│   ├── routers/
│   │   └── auth.py         # /auth/* endpoints
│   └── main.py             # App factory
├── alembic/                 # Migrations
├── scripts/
│   ├── start.sh            # Entrypoint Railway/production
│   ├── wait-for-postgres.sh # Entrypoint local Docker
│   └── create_admin.py     # Create admin interactively
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## PT-BR

### Como usar

#### 1. Copiar o template

```bash
cp -r fastapi-skeleton meu-novo-projeto
cd meu-novo-projeto
```

#### 2. Personalizar

Editar estes valores para o seu projeto:

| Arquivo | O que mudar |
|---|---|
| `.env.example` → `.env` | `POSTGRES_DB`, `SECRET_KEY` |
| `app/main.py` | `title`, `description` |
| `app/core/config.py` | `postgres_db` default |
| `alembic.ini` | `sqlalchemy.url` (nome do banco) |
| `docker-compose.yml` | Portas se necessário |

#### 3. Criar o `.env`

```bash
cp .env.example .env
# Editar o .env com os valores do seu projeto
```

#### 4. Subir com Docker

```bash
docker compose up --build
```

A API estará em `http://localhost:8000/docs`.

#### 5. Criar a primeira migration

```bash
docker compose exec web alembic revision --autogenerate -m "create users and roles"
docker compose exec web alembic upgrade head
```

#### 6. Criar o admin

```bash
docker compose exec web python scripts/create_admin.py
```

#### 7. Testar login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "seu@email.com", "password": "suasenha"}'
```

### Comandos úteis

```bash
# Subir
docker compose up

# Rebuild após mudar requirements.txt
docker compose up --build

# Nova migration
docker compose exec web alembic revision --autogenerate -m "descricao"

# Rodar migrations
docker compose exec web alembic upgrade head

# Rollback última migration
docker compose exec web alembic downgrade -1

# Shell Python dentro do container
docker compose exec web python

# Logs
docker compose logs -f web
```

### Adicionando novos modelos

1. Criar o model em `app/models/meu_model.py`
2. Importar no `app/main.py` (registro no SQLAlchemy)
3. Importar no `alembic/env.py` (autogenerate)
4. Gerar migration: `docker compose exec web alembic revision --autogenerate -m "add meu_model"`
5. Aplicar: `docker compose exec web alembic upgrade head`

### Adicionando novos routers

1. Criar o router em `app/routers/meu_router.py`
2. Registrar no `app/main.py`: `app.include_router(meu_router.router)`

### Deploy (Railway)

O Dockerfile detecta automaticamente o Railway via `DATABASE_URL`:
- Roda migrations antes de iniciar
- Suporta `PROCESS_TYPE=web` ou `PROCESS_TYPE=worker`

Variáveis obrigatórias em produção:
- `DATABASE_URL` (Railway configura automaticamente)
- `SECRET_KEY` (gerar com `openssl rand -hex 32`)
- `ENVIRONMENT=production`
- `CORS_ORIGINS` (URLs do frontend)

---

## EN

### How to use

#### 1. Copy the template

```bash
cp -r fastapi-skeleton my-new-project
cd my-new-project
```

#### 2. Customize

Edit these values for your project:

| File | What to change |
|---|---|
| `.env.example` → `.env` | `POSTGRES_DB`, `SECRET_KEY` |
| `app/main.py` | `title`, `description` |
| `app/core/config.py` | `postgres_db` default |
| `alembic.ini` | `sqlalchemy.url` (database name) |
| `docker-compose.yml` | Ports if needed |

#### 3. Create the `.env`

```bash
cp .env.example .env
# Edit .env with your project values
```

#### 4. Start with Docker

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000/docs`.

#### 5. Create the first migration

```bash
docker compose exec web alembic revision --autogenerate -m "create users and roles"
docker compose exec web alembic upgrade head
```

#### 6. Create the admin

```bash
docker compose exec web python scripts/create_admin.py
```

#### 7. Test login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "your@email.com", "password": "yourpassword"}'
```

### Useful commands

```bash
# Start
docker compose up

# Rebuild after changing requirements.txt
docker compose up --build

# New migration
docker compose exec web alembic revision --autogenerate -m "description"

# Run migrations
docker compose exec web alembic upgrade head

# Rollback last migration
docker compose exec web alembic downgrade -1

# Python shell inside container
docker compose exec web python

# Logs
docker compose logs -f web
```

### Adding new models

1. Create the model in `app/models/my_model.py`
2. Import in `app/main.py` (SQLAlchemy registration)
3. Import in `alembic/env.py` (autogenerate)
4. Generate migration: `docker compose exec web alembic revision --autogenerate -m "add my_model"`
5. Apply: `docker compose exec web alembic upgrade head`

### Adding new routers

1. Create the router in `app/routers/my_router.py`
2. Register in `app/main.py`: `app.include_router(my_router.router)`

### Deploy (Railway)

The Dockerfile automatically detects Railway via `DATABASE_URL`:
- Runs migrations before starting
- Supports `PROCESS_TYPE=web` or `PROCESS_TYPE=worker`

Required production variables:
- `DATABASE_URL` (Railway configures automatically)
- `SECRET_KEY` (generate with `openssl rand -hex 32`)
- `ENVIRONMENT=production`
- `CORS_ORIGINS` (frontend URLs)

---

## Ports

| Service | Container | Host (default) | Where to change |
|---|---|---|---|
| **PostgreSQL** | `5432` | `5432` | `docker-compose.yml` → `db.ports` |
| **FastAPI** | `8000` | `8000` | `docker-compose.yml` → `web.ports` + `web.environment.PORT` + `Dockerfile` → `ENV PORT` |

To change the host port (e.g. to run multiple projects at the same time), edit only the left side of the mapping in `docker-compose.yml`:

Para mudar a porta do host (ex: rodar vários projetos ao mesmo tempo), edite apenas o lado esquerdo do mapeamento em `docker-compose.yml`:

```yaml
# PostgreSQL on host port 5439
db:
  ports:
    - '5439:5432'

# API on host port 8080
web:
  ports:
    - '8080:8000'
  environment:
    - PORT=8000  # internal container port, no need to change
```
