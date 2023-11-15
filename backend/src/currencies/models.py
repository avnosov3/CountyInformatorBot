from django.db import models

from core import models_constants


class Currency(models.Model):
    code = models.CharField(max_length=models_constants.CURRENCY_CODE_LENGTH, null=True, blank=True, verbose_name="Код")

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"

    def __str__(self):
        return str(self.code)
