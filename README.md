# Countries Informator Bot
![Static Badge](https://img.shields.io/badge/Language-Python_3.10-blue)
![Static Badge](https://img.shields.io/badge/Framework-Django_Ninja-3CB371)
![Static Badge](https://img.shields.io/badge/SQL_Database-PostgreSQL-6495ED)
![Static Badge](https://img.shields.io/badge/ORM-Django_ORM-DC143C)
![Static Badge](https://img.shields.io/badge/NoSQL_Database-Redis-B22222)
![Static Badge](https://img.shields.io/badge/Task_manager-Celery-ADFF2F)

## Chatbot for up-to-date country information

The bot allows you to get information about countries, counties and cities.

Information includes:
* Current weather information
* Information on the currency used and the exchange rate against the dollar
* Brief information about the locality

## External APIs

- [FreecurrencyAPI](https://freecurrencyapi.com/docs/#official-libraries)
- [Restful Countries API](https://restfulcountries.com/api-documentation/version/1)
- [GeoDB](https://rapidapi.com/wirefreethought/api/geodb-cities/)
- [OpenWeather API](https://openweathermap.org/api)


## Technologies

- [Python 3.10](https://github.com/python/cpython)
- [Django Ninja 0.22.2](https://github.com/vitalik/django-ninja)
- [PostgreSQL 15-alpine](https://hub.docker.com/_/postgres)
- [Redis 7.2.1-alpine](https://github.com/redis/redis)
- [Celery 5.3.4](https://github.com/celery/celery)

## Project outline

![](https://drive.google.com/uc?export=view&id=1UehRCVG-cxNmUzaRtuXfh2iR-51a9kaG)

## Database diaograms

![](https://drive.google.com/uc?export=view&id=1GmMzrOFkA0xkEcbtSVRbH7Wv3a_y1IIw)

## Run docker compose

- Rename the `.env.example` file to `.env` and pass the variables their values
- Or create a `.env` file in the root of the project

- Minimum environment variables to be written into `.env` to start the project:
```shell
# db conf
DB_USER=
DB_PASSWORD=
DB_NAME= 
DB_HOST=db
DB_PORT=543 
ENGINE=django.db.backends.postgresql 
POSTGRES_HOST_AUTH_METHOD=
POSTGRES_INITDB_ARGS=

# app conf
API_HOST=backend
API_PORT=8000
API_VERSION=
BACKEND_COUNTRY_URL=
BACKEND_CURRENCY_URL=
BACKEND_CURRENCY_URL=
BACKEND_CITY_URL=
BACKEND_WEATHER_URL=
CITIES_AMOUNT=1

# bot conf
BOT_API_TOKEN=
BOT_REDIS_DB=

# django conf
SECRET_KEY=
DEBUG=1

LIST_PER_PAGE=

DJANGO_ADMIN=
DJANGO_ADMIN_EMAIL=
DJAGO_ADMIN_PASSWORD=

# redis conf
REDIS_HOST=redis
REDIS_PORT=6379

CACHE_ENABLE=
DEFAULT_CACHE_URL=

CURRENCIES_CACHE_URL=
CURRENCY_TIMEOUT=

WEATHER_CACHE_URL=
WEATHER_CACHE_TIMEOUT=

COUNTRIES_TIMEOUT=
CITIES_TIMEOUT=

# flower conf
CELERY_BROKER_URL=redis://${REDIS_HOST}:${REDIS_PORT}//
CELERY_RETRY_ATTEMPTS=
CELERY_WAITING_TIME_BEFORE_NEW_ATTEMPTS=
FLOWER_PORT=5555

ENVIRONMENT=DEV

# api urls
SLEEP_TIME=

COUNTRIES_API=https://restcountries.com/v3.1/all

CITIES_API=https://wft-geo-db.p.rapidapi.com/v1/geo/cities
CITY_MIN_POPULATION=
CITY_ORDER=
CITY_TYPES=
CITY_LIMIT=
CITY_API_KEY=
CITY_API_KEY_VALUE=
CITY_API_HOST_KEY=
CITY_API_HOST_VALUE=
REGION_API=https://wft-geo-db.p.rapidapi.com/v1/geo/countries

CURRENCY_API=
CURRENCY_API_KEY=
CURRENCY_API_TOKEN=

WEATHER_API_KEY=
WEATHER_API_TOKEN=
WEATHER_API_URL=https://api.api-ninjas.com/v1/weather
```


## Once launched, there will be access to:
* [Documentation (Swagger)](http://127.0.0.1:8000/api/v1/docs)
* [Documentation (Redoc)](http://127.0.0.1:8000/api/v1/redoc/)
* [Admin-panel django](http://127.0.0.1:8000/admin/)
* [Admin-panel postgres](http://127.0.0.1:8080/adminer/)
* [Flower](http://127.0.0.1:5555/)
