import unittest
from category.domain.entities import Category
from __seedwork.domain.exceptions import ValidationException


class TestCategoryIntegration(unittest.TestCase):

    def test_return_error_when_name_is_non_required_and_over_size_limit(self):
        with self.assertRaises(ValidationException) as exception:
            Category(name=None)
        self.assertEqual(
            "Property name is required",
            str(exception.exception.args[0]),
        )

        with self.assertRaises(ValidationException) as exception:
            Category(name="")
        self.assertEqual(
            "Property name is required",
            str(exception.exception.args[0]),
        )

        with self.assertRaises(ValidationException) as exception:
            Category(name="Any" * 100)
        self.assertEqual(
            "Property name must be less than 255 chars",
            str(exception.exception.args[0]),
        )
        with self.assertRaises(ValidationException) as exception:
            Category(name=5)
        self.assertEqual(
            "Property name must be a string",
            str(exception.exception.args[0]),
        )

    def test_return_error_when_description_is_not_string(self):
        with self.assertRaises(ValidationException) as exception:
            Category(name="Test", description=5)
        self.assertEqual(
            "Property description must be a string",
            str(exception.exception.args[0]),
        )
