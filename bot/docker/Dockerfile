FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONBUFFERED 1

RUN apt-get -y update; apt-get -y install curl

RUN pip install poetry==1.5.1

COPY ./poetry.lock ./pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-ansi --no-root --only main

COPY ./src ./src

# COPY docker/bot_entrypoint.sh ./

# RUN chmod +x bot_entrypoint.sh
