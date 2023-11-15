import random

import factory

from cities.models import City
from countries.tests.factories import StateFactory


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = random.choice(("Asia", "Europe", "Africa"))
    code = random.randint(0, 100000)
    population = random.randint(0, 100000)
    state = factory.SubFactory(StateFactory)
    latitude = random.choice((23.45, 34.54, 465.4))
    longitude = random.choice((23.45, 34.54, 465.4))
    utc = random.choice(("+03:00", "+04:00"))
