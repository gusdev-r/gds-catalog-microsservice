import unittest
from category.domain.entities import Category
from __seedwork.domain.exceptions import ValidationException


class TestCategoryIntegration(unittest.TestCase):
    def test_return_error_when_name_is_not_valid_prop_cases(self):
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

    def test_return_error_when_description_is_not_valid_prop_cases(self):
        with self.assertRaises(ValidationException) as exception:
            Category(name="Test", description=5)
        self.assertEqual(
            "Property description must be a string",
            str(exception.exception.args[0]),
        )

    def test_create_with_valid_cases(self):
        try:
            Category(name="Test")
            Category(name="Test", description=None)
            Category(name="Test", description="")
            Category(name="Test", is_active=True)
            Category(name="Test", is_active=False)
            Category(name="Test", description="Test Description", is_active=False)
        except ValidationException as exception:
            self.fail(f"Some prop is not valid. Error: {exception.args[0]}")

    def test_return_error_when_name_is_not_valid_update_function_cases(self):
        category = Category(name="Test")
        with self.assertRaises(ValidationException) as exception:
            category.update(name=None, description=None)
        self.assertEqual(
            "Property name is required",
            str(exception.exception.args[0]),
        )

        with self.assertRaises(ValidationException) as exception:
            category.update(name="", description=None)
        self.assertEqual(
            "Property name is required",
            str(exception.exception.args[0]),
        )

        with self.assertRaises(ValidationException) as exception:
            category.update(name="10" * 200, description=None)
        self.assertEqual(
            "Property name must be less than 255 chars",
            str(exception.exception.args[0]),
        )
        with self.assertRaises(ValidationException) as exception:
            category.update(name=5, description=None)
        self.assertEqual(
            "Property name must be a string",
            str(exception.exception.args[0]),
        )

    def test_return_error_when_description_is_not_valid_update_cases(self):
        category = Category(name="Test", description="Test description")
        with self.assertRaises(ValidationException) as exception:
            category.update(name=category.name, description=5)
        self.assertEqual(
            "Property description must be a string",
            str(exception.exception.args[0]),
        )

    def test_update_with_valid_cases(self):
        category = Category(name="Test")
        try:
            category.update(name="Test", description=None)
            category.update(name="Test", description="Test Description")
            category.update(name="Test", description=None)
            category.update(name="Test", description="")
        except ValidationException as exception:
            self.fail(f"Some prop is not valid. Error: {exception.args[0]}")
