#!/bin/bash

python3 manage.py migrate
python3 manage.py filladmin

python /tmp/debugpy --wait-for-client --listen 0.0.0.0:5678 -m uvicorn core.asgi:application --host "${API_HOST:-0.0.0.0}" --port "${API_PORT:-8000}" --reload
