# python-fastapi-sample-app

Huong dan setup va config cho project FastAPI.

## 1. Yeu cau moi truong

- Python 3.10+ (khuyen nghi 3.11)
- pip

## 2. Cau truc thu muc

```text
app/
	main.py
	api/
		router.py
		routes/
			health.py
			users.py
	core/
		config.py
		lifespan.py
	schemas/
		user.py
	services/
		user_service.py
```

## 3. Cai dat project

### Buoc 1: Tao virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### Buoc 2: Cai dependencies

```bash
pip install fastapi uvicorn pydantic-settings
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
DATABASE_URL=
```

## 4. Chay ung dung

```bash
uvicorn app.main:app --reload
```

URL mac dinh:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## 5. API hien co

- GET /api/v1/health/
- GET /api/v1/users/me
- PATCH /api/v1/users/me
- GET /api/v1/workspaces/
- POST /api/v1/workspaces/ (query param: name)
- POST /api/v1/workspaces/{workspace_id}/members (query param: user_id)
- DELETE /api/v1/workspaces/{workspace_id}/members/{user_id}
