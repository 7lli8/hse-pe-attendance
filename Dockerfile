FROM python:3.12-slim

RUN pip3 install poetry

WORKDIR /app
COPY poetry.lock /app/
COPY pyproject.toml /app/

RUN poetry install --without dev --no-root

COPY . /app

CMD ["poetry", "run", "python", "main.py"]