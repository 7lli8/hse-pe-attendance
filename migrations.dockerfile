FROM python:3.12-slim

RUN apt install -y python3-dev libpq-dev

RUN pip3 install poetry

WORKDIR /app
COPY poetry.lock /app/
COPY pyproject.toml /app/

RUN poetry install --without dev --no-root

COPY . /app

CMD ["poetry", "run", "alembic", "upgrade", "head"]