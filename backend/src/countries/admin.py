from django.contrib import admin
from django.core.cache import caches
from django.db.models import QuerySet
from django.http import HttpRequest
from django_object_actions import DjangoObjectActions, action

from core.settings import LIST_PER_PAGE
from countries import models
from countries.apps import CountriesConfig


@admin.register(models.Country)
class CountryAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ("id", "name", "capital", "continent", "population", "size", "phone_code")
    list_display_links = ("name",)
    autocomplete_fields = ("languages", "currency")
    list_filter = ("continent",)
    search_fields = ("name", "full_name", "languages__name", "capital", "currency__code")
    list_per_page = LIST_PER_PAGE
    empty_value_display = "-пусто-"

    @action(label="Очистить кеш стран")
    def clear_countries_cache(self, request: HttpRequest, queryset: QuerySet):
        caches[CountriesConfig.name].clear()

    changelist_actions = ("clear_countries_cache",)


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_per_page = LIST_PER_PAGE
    empty_value_display = "-пусто-"


@admin.register(models.State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country", "num_cities")
    list_display_links = ("name",)
    search_fields = ("name", "country__name")
    autocomplete_fields = ("country",)
    list_per_page = LIST_PER_PAGE
    empty_value_display = "-пусто-"


@admin.register(models.Continent)
class ContinentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("name",)
    list_per_page = LIST_PER_PAGE
    empty_value_display = "-пусто-"
