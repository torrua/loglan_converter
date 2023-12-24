# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from __future__ import annotations
from typing import Iterable
from app.models.storage.properties import (
    TableProperties,
    DEFAULT_TABLE_PROPERTIES_COLLECTION,
)
from app.models.storage.table_container import TableContainer


class Storage:
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

        containers = TableContainer.generate_containers(table_properties_collection)

        if len(containers) != 8:
            raise ValueError("Insufficient table contents generated.")

        self.author = containers[0]
        self.event = containers[1]
        self.word_type = containers[2]
        self.word = containers[3]
        self.word_spell = containers[4]
        self.definition = containers[5]
        self.settings = containers[6]
        self.syllable = containers[7]

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

    @property
    def containers(self) -> list[TableContainer]:
        return sorted(
            [v for v in self.__dict__.values() if isinstance(v, TableContainer)],
            key=lambda v: v.order,
        )

    def container_by_name(self, name) -> TableContainer:
        for container in self.containers:
            if container.name == name:
                return container

        raise ValueError(f"Container '{name}' not found.")
