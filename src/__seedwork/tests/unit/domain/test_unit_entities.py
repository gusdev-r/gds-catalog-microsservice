import unittest
from abc import ABC
from domain.entities import Entity
from dataclasses import is_dataclass
import unittest
from unittest.mock import patch
import uuid
from domain.value_objects import UniqueEntityId
from domain.exceptions import InvalidUuidException
from dataclasses import FrozenInstanceError, is_dataclass


class TestUniqueEntityId(unittest.TestCase):
    def test_if_is_instance_of_abc(self):
        self.assertIsInstance(Entity(), ABC)

    def test_if_is_dataclass(self):
        self.assertTrue(is_dataclass(Entity))

    def test_if_is_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_throw_exception_when_uuid_is_invalid(self):
        with patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate",
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate,
        ) as mock_validate:
            with self.assertRaises(InvalidUuidException) as assert_error:
                UniqueEntityId("Invalid id")
        mock_validate.assert_called_once()
        self.assertEqual(assert_error.exception.args[0], "Id must be a valid UUID")

    def test_accept_uuid_when_passed_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate",
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate,
        ) as mock_validate:
            with self.assertRaises(InvalidUuidException):
                UniqueEntityId("invalid id")
        value_object = UniqueEntityId("bbeb03a4-d8f6-4df8-af2c-2620acf9b191")
        mock_validate.assert_called_once()
        self.assertEqual("bbeb03a4-d8f6-4df8-af2c-2620acf9b191", value_object.id)

    def test_uuid_as_string_when_is_created(self):
        uuid_value = uuid.uuid4()
        value_object = UniqueEntityId(uuid_value)
        self.assertEqual(value_object.id, str(uuid_value))

    def test_generate_id_when_no_passed_id_in_constructor(self):
        with patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate",
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate,
        ) as mock_validate:
            value_object = UniqueEntityId()
            uuid.UUID(value_object.id)
            mock_validate.assert_called_once()

    def test_if_value_object_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = UniqueEntityId()
            value_object.id = "Invalid id"
