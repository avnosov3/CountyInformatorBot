import random

import factory

from countries.models import Continent, Country, Language, State
from currencies.models import Currency


class ContinentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Continent
        django_get_or_create = ("name",)

    name = random.choice(("Asia", "Europe", "Africa"))


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Currency
        django_get_or_create = ("code",)

    code = random.choice(("usd", "eur", "rub"))


class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Language
        django_get_or_create = ("name",)

    name = random.choice(("English", "Spanish", "French"))


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country

    name = factory.Faker("country")
    full_name = factory.Faker("country")
    capital = factory.Faker("city")
    continent = factory.SubFactory(ContinentFactory)
    population = random.randint(0, 100000)
    size = random.randint(0, 100000)
    code = factory.Sequence(lambda n: f"u{n}")
    phone_code = factory.Sequence(lambda n: f"+{n}")
    currency = factory.SubFactory(CurrencyFactory)

    @factory.post_generation
    def languages(self, create, value, **kwargs):
        if not create:
            return
        if value:
            self.languages.set(value)


class StateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = State
        django_get_or_create = ("name",)

    name = random.choice(("Moscow", "Vologda", "Omsk"))
    num_cities = random.randint(0, 100000)
    country = factory.SubFactory(CountryFactory)
