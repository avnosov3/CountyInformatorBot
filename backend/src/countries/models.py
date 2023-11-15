from django.db import models

from core import models_constants


class Continent(models.Model):
    name = models.CharField(max_length=models_constants.NAME_BASE_LENGTH, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Континент"
        verbose_name_plural = "Континенты"

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=models_constants.NAME_BASE_LENGTH, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(
        max_length=models_constants.NAME_BASE_LENGTH, null=True, blank=True, verbose_name="Название"
    )
    full_name = models.CharField(
        max_length=models_constants.NAME_BASE_LENGTH, null=True, blank=True, verbose_name="Полное название"
    )
    capital = models.CharField(
        max_length=models_constants.NAME_BASE_LENGTH,
        null=True,
        blank=True,
        verbose_name="Столица",
    )
    continent = models.ForeignKey(
        Continent,
        null=True,
        blank=True,
        related_name="countries",
        on_delete=models.CASCADE,
        verbose_name="Континент",
    )
    population = models.PositiveIntegerField(verbose_name="Население", null=True, blank=True)
    size = models.PositiveBigIntegerField(verbose_name="Размер", null=True, blank=True)
    code = models.CharField(max_length=models_constants.COUNTRY_CODE_LENGTH, unique=True, verbose_name="Код")
    phone_code = models.CharField(
        max_length=models_constants.COUNTRY_PHONE_CODE_LENGTH, null=True, blank=True, verbose_name="Телефонный код"
    )
    currency = models.ForeignKey(
        "currencies.Currency",
        null=True,
        blank=True,
        related_name="country",
        on_delete=models.SET_NULL,
        verbose_name="Валюта",
    )
    languages = models.ManyToManyField(Language, related_name="countries", verbose_name="Языки")

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return str(self.name)


class State(models.Model):
    name = models.CharField(
        max_length=models_constants.NAME_BASE_LENGTH, null=True, blank=True, verbose_name="Название"
    )
    code = models.CharField(max_length=models_constants.STATE_CODE_LENGTH, verbose_name="Код")
    num_cities = models.PositiveIntegerField(verbose_name="Количество городов")
    country = models.ForeignKey(
        Country,
        null=True,
        blank=True,
        related_name="states",
        on_delete=models.CASCADE,
        verbose_name="Страна",
    )

    class Meta:
        verbose_name = "Область"
        verbose_name_plural = "Области"

    def __str__(self):
        return f"{self.country} - {str(self.name)}"
