import unittest

from parser.exceptions import (NotListOfDictsException,
                               NotDictException,
                               DuplicatedKeysException,
                               KeysNotFoundException)
from parser.parser import JsonParser


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = JsonParser()
        self.test_keys = ['currency', 'country', 'city']

    def test_parse_one_currency(self):
        currency = [{
            "country": "FR",
            "city": "Paris",
            "currency": "EUR",
            "amount": 20
        }]

        answer = self.parser.parse(currency, self.test_keys)
        expected = {"EUR": {
            "FR": {
                "Paris": [
                    {
                        "amount": 20
                    }
                ]
            }
        }}
        self.assertEqual(expected, answer)

    def test_parse_two_currencies(self):
        currencies = [
            {
                "country": "UK",
                "city": "London",
                "currency": "GBP",
                "amount": 12.2
            },
            {
                "country": "FR",
                "city": "Paris",
                "currency": "EUR",
                "amount": 20
            },
        ]
        expected = {
            "GBP": {
                "UK": {
                    "London": [
                        {
                            "amount": 12.2
                        }
                    ]
                }
            },
            "EUR": {
                "FR": {
                    "Paris": [
                        {
                            "amount": 20
                        }
                    ]
                }
            },
        }
        answer = self.parser.parse(currencies, self.test_keys)
        self.assertEqual(expected, answer)

    def test_add_two_countries_with_same_currency(self):
        currencies = [
            {
                "country": "ES",
                "city": "Madrid",
                "currency": "EUR",
                "amount": 8.9
            },
            {
                "country": "FR",
                "city": "Paris",
                "currency": "EUR",
                "amount": 20
            }]
        expected = {
            'ES':
                {'Madrid':
                    [
                        {'amount': 8.9,
                         'currency': 'EUR'
                         }
                    ]
                },
            'FR':
                {
                    'Paris':
                        [
                            {'amount': 20,
                             'currency': 'EUR'
                             }
                        ]
                }
        }

        answer = self.parser.parse(currencies, ["country", "city"])
        self.assertDictEqual(expected, answer)

    def test_raise_not_list_of_dicts_exception(self):
        with self.assertRaises(NotListOfDictsException):
            answer = self.parser.parse({"a", "b"}, keys=['a'])

    def test_raise_not_nested_dict_exception(self):
        with self.assertRaises(NotDictException):
            answer = self.parser.parse([["a", "b"]], keys=['a'])

    def test_test_raise_duplicated_keys_exception(self):
        with self.assertRaises(DuplicatedKeysException):
            answer = self.parser.parse([{"a": 123}, {"a": 229}],
                                       keys=["a", "a"])

    def test_raise_keys_not_found_exception(self):
        with self.assertRaises(KeysNotFoundException):
            answer = self.parser.parse([{"a": 123}, {"a": 229}],
                                       keys=["b"])
