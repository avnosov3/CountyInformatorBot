from django.db import models

from core import models_constants


class City(models.Model):
    name = models.CharField(max_length=models_constants.NAME_BASE_LENGTH, verbose_name="Название")
    code = models.IntegerField("Код города", null=True, blank=True)
    population = models.PositiveIntegerField(verbose_name="Население")
    state = models.ForeignKey(
        "countries.State",
        null=True,
        blank=True,
        related_name="cities",
        on_delete=models.CASCADE,
        verbose_name="Регион",
    )
    latitude = models.FloatField(max_length=models_constants.COORDINATE_LENGTH, verbose_name="Широта")
    longitude = models.FloatField(max_length=models_constants.COORDINATE_LENGTH, verbose_name="Долгота")
    utc = models.CharField(
        max_length=models_constants.UTC_LENGTH,
        null=True,
        blank=True,
        verbose_name="UTC",
    )

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        constraints = [
            models.UniqueConstraint(
                name="Проверка уникальности координат",
                fields=["latitude", "longitude"],
            )
        ]

    def __str__(self):
        return self.name
