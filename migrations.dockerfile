FROM python:3.12-slim

RUN apt-get update && apt-get install -y python3-dev libpq-dev build-essential

RUN pip3 install poetry


WORKDIR /app
COPY poetry.lock /app/
COPY pyproject.toml /app/

RUN poetry install --no-root

COPY . /app

CMD ["poetry", "run", "alembic", "upgrade", "head"]