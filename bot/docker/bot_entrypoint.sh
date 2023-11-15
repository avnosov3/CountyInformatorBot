#!/bin/bash


check_backend() {
  local backend_host="${API_HOST:-backend}"
  local backend_port="${API_PORT:-8000}"
  local healthcheck="$backend_host:$backend_port/${HEALTHCHECK_ENDPOINT}"
  local max_attempts=10
  local delay=5
  local attempt=0

  echo "Ожидание запуска бэкенда на $healthcheck"

  while [ "$attempt" -lt "$max_attempts" ]; do

    if curl -s "http://$healthcheck" | grep -q 'pong'; then
      echo "Бэкенд доступен, запуск бота."
      return 0
    fi

    sleep "$delay"
    ((attempt++))
  done

  echo "Не удалось дождаться запуска бэкенда после $max_attempts попыток."
  return 1
}


if check_backend; then

  echo "Запуск бота..."
  python3 main.py
else

  exit 1
fi