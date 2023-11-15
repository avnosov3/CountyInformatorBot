#!/bin/bash

python3 manage.py migrate
python3 manage.py filladmin

uvicorn core.asgi:application --host "${API_HOST:-0.0.0.0}" --port "${API_PORT:-8000}"
