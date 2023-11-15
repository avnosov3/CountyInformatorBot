from django.test import TestCase

from countries.models import Country
from countries.repository import country_repository
from countries.schemas import CountryInSchema
from countries.tests.fixtures import CREATE_COUNTRIES, FIRST_COUNTRY_CODE, SECOND_COUNTRY_CODE, UPDATE_COUNTRIES


class CountryRepositoryTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.countries_in_for_create = [CountryInSchema(**data) for data in CREATE_COUNTRIES]
        cls.countries_in_for_update = [CountryInSchema(**data) for data in UPDATE_COUNTRIES]

    def get_country_with_languages_by_name(self, code):
        return (
            Country.objects.select_related(
                "continent",
                "currency",
            )
            .prefetch_related("languages")
            .filter(code=code)
            .first()
        )

    def test_create_countries(self):
        countries = country_repository.create_countries(self.countries_in_for_create)
        countries_with_languages_for_create = (
            Country.objects.select_related(
                "continent",
                "currency",
            )
            .prefetch_related("languages")
            .all()
        )
        self.assertEqual(len(countries), len(countries_with_languages_for_create))
        for created_country, expected_country in zip(countries, countries_with_languages_for_create):
            for value, excepted in (
                (created_country.name, expected_country.name),
                (created_country.full_name, expected_country.full_name),
                (created_country.capital, expected_country.capital),
                (created_country.population, expected_country.population),
                (created_country.size, expected_country.size),
                (created_country.code, expected_country.code),
                (created_country.phone_code, expected_country.phone_code),
                (created_country.currency, expected_country.currency),
                (created_country.languages, expected_country.languages),
            ):
                with self.subTest(value=value, excepted=excepted):
                    self.assertEqual(value, excepted)

    def test_update_countries(self):
        country_repository.create_countries(self.countries_in_for_create)
        first_update_country, second_update_country = country_repository.update_countries(self.countries_in_for_update)
        first_country = self.get_country_with_languages_by_name(FIRST_COUNTRY_CODE)
        second_country = self.get_country_with_languages_by_name(SECOND_COUNTRY_CODE)
        for value, excepted in (
            (first_update_country.name, first_country.name),
            (first_update_country.full_name, first_country.full_name),
            (first_update_country.capital, first_country.capital),
            (first_update_country.population, first_country.population),
            (first_update_country.size, first_country.size),
            (first_update_country.code, first_country.code),
            (first_update_country.phone_code, first_country.phone_code),
            (first_update_country.currency, first_country.currency),
            (first_update_country.languages, first_country.languages),
            (second_update_country.name, second_country.name),
            (second_update_country.full_name, second_country.full_name),
            (second_update_country.capital, second_country.capital),
            (second_update_country.population, second_country.population),
            (second_update_country.size, second_country.size),
            (second_update_country.code, second_country.code),
            (second_update_country.phone_code, second_country.phone_code),
            (second_update_country.currency, second_country.currency),
            (second_update_country.languages, second_country.languages),
        ):
            with self.subTest(value=value, excepted=excepted):
                self.assertEqual(value, excepted)
