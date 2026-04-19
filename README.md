A modular backend system built using FastAPI, covering authentication, blog APIs, caching, and reusable backend services.
## Features

- Blog API (CRUD operations)
- JWT Authentication & Authorization
- Role-based access control
- Redis caching layer
- Modular architecture
- PostgreSQL database integration
- API documentation (Swagger UI)

- ## Tech Stack

- FastAPI
- Python 3.10+
- PostgreSQL
- Redis
- JWT (Authentication)
- SQLAlchemy / ORM

- ## Project Structure

blog_project/     -> Blog APIs  
auth_jwt/         -> Authentication system  
redis_module/     -> Caching layer  
utils/            -> Helper functions  

## Installation

git clone https://github.com/your-username/repo-name.git
cd repo-name

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload
