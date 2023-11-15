from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    BOT_API_TOKEN: str

    REDIS_HOST: str
    REDIS_PORT: str
    BOT_REDIS_DB: str

    API_HOST: str
    API_PORT: str
    API_VERSION: str

    BACKEND_COUNTRY_URL: str
    BACKEND_CURRENCY_URL: str
    BACKEND_CITY_URL: str
    BACKEND_WEATHER_URL: str

    CITIES_AMOUNT: int

    SERVICE_UNAVALIABLE: str

    CLIENT_TIMEOUT: int


settings = Settings()
