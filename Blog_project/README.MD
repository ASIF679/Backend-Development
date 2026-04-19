# Blog Project

A simple FastAPI backend for a blog application with user registration, authentication, and admin/user routes.

## Features

- FastAPI application
- SQLAlchemy ORM models
- JWT authentication
- Password hashing
- Admin and user route separation
- Swagger UI documentation

## Requirements

- Python 3.11+ (recommended)
- PostgreSQL or another SQLAlchemy-compatible database

## Setup

1. Create and activate a Python virtual environment.

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. Install dependencies.

   ```powershell
   pip install -r requirements.txt
   ```

3. Configure your database connection.

   Open `Database.py` and set `DatabaseURL` to your database URL, for example:

   ```python
   DatabaseURL = "postgresql+psycopg2://user:password@localhost:5432/blogdb"
   ```

4. (Optional) Update authentication settings.

   The JWT secret and token expiration are defined in `auth.py`:

   - `SECRET_KEY`
   - `ACCESS_TOKEN_EXPIRE_TIME`

## Run

Start the application with Uvicorn:

```powershell
uvicorn main:app --reload
```

Then open:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs

## API Endpoints

- `GET /` - health check endpoint
- `GET /healthcheck` - database connection check
- `POST /register_user` - register new user
- `POST /login` - authenticate and receive JWT token

Other user/admin routes are defined in `user_routes.py` and `admin_routes.py`.

## Notes

- The current project expects a valid SQLAlchemy database URL.
- Tables are created automatically when the app starts.
- Use the Swagger UI at `/docs` for interactive API testing.
