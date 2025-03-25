import unittest
from abc import ABC
from __seedwork.domain.validators import ValidatorRules
from __seedwork.domain.exceptions import ValidationException
from dataclasses import is_dataclass
import unittest
from unittest.mock import patch
import uuid


class TestValidatorRules(unittest.TestCase):
    def setUp(self):
        self.validator = ValidatorRules.values("value 1", "prop 1")
        self.invalid_data = [
            {
                "value_required": None,
                "value_string": True,
                "value_max_length": "Testing",
                "prop_default": "prop 1",
                "prop_bool": "prop_bool 1",
                "value_bool": 5,
            },
            {
                "value_required": None,
                "value_string": 10,
                "value_max_length": "Testing",
                "prop_default": "prop 2",
                "prop_bool": "prop_bool 2",
                "value_bool": "not boolean",
            },
        ]

    def test_values_method(self):
        self.assertIsInstance(self.validator, ValidatorRules)
        self.assertEqual(self.validator.value, "value 1")
        self.assertEqual(self.validator.prop, "prop 1")

    def test_required_rule(self):
        for item in self.invalid_data:
            with self.assertRaises(ValidationException) as exception:
                ValidatorRules.values(
                    item["value_required"], item["prop_default"]
                ).required()

        self.assertEqual(
            f"Property {item['prop_default']} is required",
            str(exception.exception.args[0]),
        )

    def test_boolean_rule(self):
        for item in self.invalid_data:
            with self.assertRaises(ValidationException) as exception:
                ValidatorRules.values(item["value_bool"], item["prop_bool"]).boolean()
        self.assertEqual(
            f"Property {item['prop_bool']} must be a boolean",
            str(exception.exception.args[0]),
        )

    def test_string_rule(self):
        for item in self.invalid_data:
            with self.assertRaises(ValidationException) as exception:
                ValidatorRules.values(
                    item["value_string"], item["prop_default"]
                ).string()

        self.assertEqual(
            f"Property {item['prop_default']} must be a string",
            str(exception.exception.args[0]),
        )

    def test_rules_in_sequence(self):
        for item in self.invalid_data:
            with self.assertRaises(ValidationException) as exception:
                ValidatorRules.values(
                    item["value_required"], item["prop_default"]
                ).required().string()

            self.assertEqual(
                f"Property {item['prop_default']} is required",
                str(exception.exception.args[0]),
            )
        for item in self.invalid_data:
            with self.assertRaises(ValidationException) as exception:
                ValidatorRules.values(
                    item["value_max_length"], item["prop_default"]
                ).required().string().max_length(5)

            self.assertEqual(
                f"Property {item['prop_default']} must be less than 5 chars",
                str(exception.exception.args[0]),
            )

        for item in self.invalid_data:
            with self.assertRaises(ValidationException) as exception:
                ValidatorRules.values(
                    item["value_string"], item["prop_default"]
                ).required().string()

            self.assertEqual(
                f"Property {item['prop_default']} must be a string",
                str(exception.exception.args[0]),
            )

        for item in self.invalid_data:
            with self.assertRaises(ValidationException) as exception:
                ValidatorRules.values(
                    item["value_bool"], item["prop_bool"]
                ).required().boolean()

            self.assertEqual(
                f"Property {item['prop_bool']} must be a boolean",
                str(exception.exception.args[0]),
            )
