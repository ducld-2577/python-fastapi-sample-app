# python-fastapi-sample-app

Huong dan setup va config cho project FastAPI.

## 1. Yeu cau moi truong

- Python 3.10+ (khuyen nghi 3.11)
- pip
- Docker + Docker Compose (de chay MySQL local)

## 2. Cau truc thu muc

```text
docker-compose.yml
README.md
alembic.ini
alembic/
	README
	env.py
	script.py.mako
	versions/
app/
	main.py
	api/
		dependencies.py
		router.py
		routes/
			health.py
			users.py
			workspace.py
	core/
		config.py
		lifespan.py
	db/
		base.py
		session.py
	models/
		base.py
		user.py
		workspace.py
	repositories/
		base.py
		user.py
		workspace.py
	schemas/
		user.py
		workspace.py
	services/
		user_service.py
		workspace_service.py
```

## 3. Cai dat project

### Buoc 1: Tao virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### Buoc 2: Cai dependencies

```bash
pip install fastapi uvicorn pydantic-settings sqlalchemy alembic pymysql aiomysql
```

### Buoc 3: Tao file .env

```bash
cp .env_example .env
```

Noi dung mau:

```env
APP_NAME=task-management-api
ENV=development
DEBUG=True

API_V1_PREFIX=/api/v1
DATABASE_URL=mysql+pymysql://taskuser:taskpass@127.0.0.1:3306/taskdb
```

### Buoc 4: Chay MySQL bang Docker

```bash
docker compose up -d mysql
```

## 4. Migration voi Alembic

### Khoi tao Alembic (chi can 1 lan)

```bash
alembic init alembic
```

Project nay da duoc khoi tao san Alembic va da co migration dau tien trong thu muc `alembic/versions/`.

### Tao migration moi tu model

```bash
alembic revision --autogenerate -m "mo_ta_thay_doi"
```

### Apply migration vao DB

```bash
alembic upgrade head
```

### Rollback 1 version

```bash
alembic downgrade -1
```

### Kiem tra version hien tai

```bash
alembic current
```

## 5. Chay ung dung

```bash
uvicorn app.main:app --reload
```

URL mac dinh:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## 6. API hien co

- GET /api/v1/health/
- GET /api/v1/users/me
- PATCH /api/v1/users/me
- GET /api/v1/workspaces/
- POST /api/v1/workspaces/ (JSON body: name)
- POST /api/v1/workspaces/{workspace_id}/members (JSON body: user_id, role)
- DELETE /api/v1/workspaces/{workspace_id}/members/{user_id}
