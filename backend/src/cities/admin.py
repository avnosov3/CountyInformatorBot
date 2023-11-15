from django.contrib import admin
from django.core.cache import caches
from django.db.models import QuerySet
from django.http import HttpRequest
from django_object_actions import DjangoObjectActions, action

from cities import models
from cities.apps import CitiesConfig
from core.settings import LIST_PER_PAGE
from weather.apps import name as weather_app


@admin.register(models.City)
class CityAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "state",
        "population",
    )
    list_display_links = ("name",)
    autocomplete_fields = ("state",)
    search_fields = ("name", "state__name", "state__country__name")
    list_per_page = LIST_PER_PAGE
    empty_value_display = "-пусто-"

    @action(label="Очистить кеш городов")
    def clear_cities_cache(self, request: HttpRequest, queryset: QuerySet):
        caches[CitiesConfig.name].clear()

    @action(label="Очистить кеш погоды")
    def clear_weather_cache(self, request: HttpRequest, queryset: QuerySet):
        caches[weather_app].clear()

    changelist_actions = ("clear_cities_cache", "clear_weather_cache")
