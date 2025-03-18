from dataclasses import FrozenInstanceError, is_dataclass
import unittest
from datetime import datetime
from category.domain.entities import Category


class TestCategory(unittest.TestCase):
    def setUp(self):
        self.fixed_datetime = datetime(2024, 3, 17, 12, 0, 0)
        self.category = Category(
            name="Movie",
            description="Movie description",
            is_active=True,
            created_at=self.fixed_datetime,
        )

    def test_category_attributes(self):
        self.assertEqual(self.category.name, "Movie")
        self.assertEqual(self.category.description, "Movie description")
        self.assertTrue(self.category.is_active)
        self.assertEqual(self.category.created_at, self.fixed_datetime)

    def test_category_string_representation(self):
        self.assertEqual(str(self.category.name), "Movie")

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor(self):
        category = Category(name="Movie")
        self.assertEqual(category.name, "Movie")
        self.assertIsNone(category.description)
        self.assertTrue(category.is_active)
        self.assertIsInstance(category.created_at, datetime)

    def test_if_created_at_is_generated_in_constructor(self):
        category_one = Category(name="Movie 1")
        category_two = Category(name="Movie 2")
        self.assertNotEqual(
            category_one.created_at.timestamp, category_two.created_at.timestamp
        )

    def test_if_category_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            category = Category(name="Immutable Movie")
            category.is_active = False
