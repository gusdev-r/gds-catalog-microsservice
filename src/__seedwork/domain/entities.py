from abc import ABC
from dataclasses import asdict, dataclass, field, fields
from typing import Any

from __seedwork.domain.value_objects import UniqueEntityId


@dataclass(frozen=True)
class Entity(ABC):
    id: UniqueEntityId = field(default_factory=lambda: UniqueEntityId())

    @property
    def id(self):
        return str(self.id)

    def _set(self, name: str, value: Any):
        object.__setattr__(self, name, value)
        return self

    def to_dict(self):
        entity_dict = asdict(self)
        entity_dict.pop("id")
        entity_dict["id"] = self.id
        return entity_dict
