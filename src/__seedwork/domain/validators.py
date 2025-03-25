from dataclasses import dataclass
from typing import Any

from .exceptions import ValidationException


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
