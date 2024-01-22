# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from __future__ import annotations

from typing import Iterable

from app.properties import (
    TableProperties,
    DEFAULT_TABLE_PROPERTIES_COLLECTION,
)
from app.table_container import TableContainer


class Storage:  # pylint: disable=too-many-instance-attributes
    def __init__(
        self,
        table_properties_collection: Iterable[
            TableProperties
        ] = DEFAULT_TABLE_PROPERTIES_COLLECTION,
    ):
        """Initialize Storage with a list of TableProperties.
        Args:
            table_properties_collection: A list of TableProperties objects.
        """

        self.containers: tuple[
            TableContainer, ...
        ] = TableContainer.generate_containers(table_properties_collection)

        if len(self.containers) != 8:
            raise ValueError("Insufficient table contents generated.")

    def __repr__(self):
        new_line = "\n\t"
        elements = new_line.join(
            [
                repr(v) + ","
                for v in self.__dict__.values()
                if isinstance(v, TableContainer)
            ]
        )
        return f"{self.__class__.__name__}({new_line}{elements}\n)"

    @property
    def names(self) -> list[str]:
        return [v.name for v in self.containers]

    def container_by_name(self, name) -> TableContainer:
        for container in self.containers:
            if container.name == name:
                return container

        raise ValueError(f"Container '{name}' not found.")
