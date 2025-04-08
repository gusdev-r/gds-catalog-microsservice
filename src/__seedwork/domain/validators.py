from abc import ABC
import abc
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, TypeVar

from .exceptions import ValidationException
from rest_framework.serializers import Serializer


@dataclass(frozen=True, slots=True)
class ValidatorRules:
    value: Any
    prop: str

    @staticmethod
    def values(value: Any, prop: str):
        return ValidatorRules(value, prop)

    def required(self) -> "ValidationException":
        if self.value is None or self.value == "":
            raise ValidationException(f"Property {self.prop} is required")
        return self

    def string(self) -> "ValidationException":
        if self.value is not None and not isinstance(self.value, str):
            raise ValidationException(f"Property {self.prop} must be a string")
        return self

    def max_length(self, max_length) -> "ValidationException":
        if self.value is not None and len(self.value) > max_length:
            raise ValidationException(
                f"Property {self.prop} must be less than {max_length} chars"
            )
        return self

    def boolean(self) -> "ValidationException":
        if (
            self.value is not None
            and self.value is not True
            and self.value is not False
        ):
            raise ValidationException(f"Property {self.prop} must be a boolean")
        return self


ErrorFields = Dict[str, List[str]]
PropsValidated = TypeVar("PropsValidated")


@dataclass(slots=True)
class ValidatorFieldsInterface(ABC, Generic[PropsValidated]):
    errors: ErrorFields
    validated_data: PropsValidated

    @abc.abstractmethod
    def validate(self, data: Any) -> bool:
        raise NotImplementedError()


class DRFValidator(ValidatorFieldsInterface[PropsValidated]):
    def validate(self, data: Serializer) -> bool:
        serializer = data
        is_valid = serializer.is_valid()

        if not is_valid:
            self.errors = {
                field: [str(_error) for _error in _errors]
                for field, _errors in serializer.errors.item()
            }
            return False
        else:
            self.validated_data = serializer.validated_data
            return True
