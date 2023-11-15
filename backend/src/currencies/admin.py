from django.contrib import admin
from django.core.cache import caches
from django.db.models import QuerySet
from django.http import HttpRequest
from django_object_actions import DjangoObjectActions, action

from core.settings import LIST_PER_PAGE
from currencies import models
from currencies.apps import CurrencyConfig


@admin.register(models.Currency)
class CurrencyAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ("id", "code")
    list_display_links = ("code",)
    search_fields = ("code",)
    list_per_page = LIST_PER_PAGE
    empty_value_display = "-пусто-"

    @action(label="Очистить кеш валют")
    def clear_currency_cache(self, request: HttpRequest, queryset: QuerySet):
        caches[CurrencyConfig.name].clear()

    changelist_actions = ("clear_currency_cache",)
