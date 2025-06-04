#  Task API

A simple and extensible Task management API built with **FastAPI**, **SQLAlchemy (async)**, and **PostgreSQL**.

Supports:
- CRUD operations for tasks
- Filtering by title and completion status
- Pagination using `fastapi-pagination`
- Background task processing
- Async database access with SQLAlchemy


## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy (async)](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [PostgreSQL](https://www.postgresql.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [FastAPI Pagination](https://fastapi-pagination.tkdodo.eu/)
- [Pytest](https://docs.pytest.org/)
- [httpx](https://www.python-httpx.org/)


## Local development

Fire up the DB with Docker:
```sh
docker-compose up -d
```

Install the dependencies:
```sh
poetry install
```

For development you will need a .env file. You can assemble it based on the testing.env file.

Start the application with:
```sh
poetry run dotenv -f .env run uvicorn task_api.app:create_app --reload --proxy-headers
```

If you are lucky enough, now you can check out the swagger:
localhost:8000/docs

Paginated endpoints can be used like this (handled by fastapi_pagination package):
localhost:8000/tasks/?size=1&page=2


### DB Migrations

DB migrations are handled by alembic.
To create a new migration file based on your models:
```sh
poetry run dotenv -f .env run alembic revision --autogenerate -m "Add tasks and task_logs"
```

To update your DB to the latest version:
```sh
poetry run dotenv -f .env run alembic upgrade head
```
These will be the most used alembic commands;
however if you did mess up something (oh, I'm pretty sure you will :)), then
head to: https://alembic.sqlalchemy.org/en/latest/

## Testing, linting
Even if there is no CI at the moment, please be so kind to run pylint and tests every once in a while:
poetry run dotenv -f testing.env run pytest -vvvs tests/test_tasks.py --asyncio-mode=auto --cov
poetry run pylint $(git ls-files '*.py')
