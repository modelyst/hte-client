#   Copyright 2022 Modelyst LLC
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import copy
from datetime import datetime
from typing import Any, List, Type

from dbgen import IDType
from dbgen.core.entity import BaseEntity, id_field
from pydantic import BaseModel, root_validator
from sqlalchemy.orm import registry
from sqlmodel import Field

from hte_client.configuration import settings

sa_registry = registry()


class SubclassBaseEntity(BaseEntity):
    @classmethod
    def subclass(
        cls,
        name: str = None,
        include: List[str] = None,
        exclude: List[str] = None,
    ) -> Type[BaseModel]:
        """Creates a subclass of this model containing only the specified fields."""
        return get_subclass(
            base=cls,
            name=name,
            include=include,
            exclude=exclude,
        )


class Base(SubclassBaseEntity):
    """A Base class that sets the ID on instantiation and whenever an ID attribute is changed."""

    id: IDType = id_field
    __schema__ = settings.POSTGRES_SCHEMA

    @root_validator
    def get_id(cls, values):
        if "id" not in values or values["id"] is None:
            values['id'] = cls._get_hash(values)
        return values

    @classmethod
    def _get_hash(cls, values):
        if cls._is_table:
            load_entity = cls._get_load_entity()
            return load_entity._get_hash(values)
        return None

    def _get_current_hash(self):
        id_dict = {key: getattr(self, key) for key in self.__identifying__}
        return self._get_hash(id_dict)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if name in self.__identifying__:
            self.id = self._get_current_hash()


class BaseTable(Base):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


def get_subclass(
    base: BaseEntity,
    name: str = None,
    include: List[str] = None,
    exclude: List[str] = None,
) -> BaseEntity:
    field_names = set(include or base.__fields__)
    excluded_fields = set(exclude or [])
    if field_names.difference(base.__fields__):
        raise ValueError(
            "Included fields not found on base class: " f"{field_names.difference(base.__fields__)}"
        )
    elif excluded_fields.difference(base.__fields__):
        raise ValueError(
            "Excluded fields not found on base class: " f"{excluded_fields.difference(base.__fields__)}"
        )
    field_names.difference_update(excluded_fields)
    new_class = type(
        name or base.__name__,
        (BaseEntity,),
        {
            "__fields__": {k: copy.copy(v) for k, v in base.__fields__.items() if k in field_names},
            '__identifying__': base.__identifying__,
        },
    )
    return new_class
