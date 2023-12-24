# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from __future__ import annotations

from typing import Any, Iterable, Sized

from app.models.storage.properties import TableProperties
from logger import log


class TableContainer(list):
    def __init__(self, table_properties: TableProperties):
        """
        Initializes the object with properties from a
        TableProperties instance.
        Parameters:
            table_properties (TableProperties): An instance of
            TableProperties containing order, name, and pattern
            attributes.
        """
        super().__init__()
        (
            self.order,
            self.name,
            self.pattern,
        ) = table_properties

    def __repr__(self):
        return f"{self.name}{self.__class__.__name__}({len(self)})"

    @property
    def number_of_items(self) -> int:
        """
        Property that returns the number of items in the 'pattern'
        attribute.
        Returns:
            int: The number of items in the 'pattern' attribute.
        """
        return len(self.pattern)

    def _is_item_suitable(self, item: Iterable[Any]) -> bool:
        """
        Determines if the given item is suitable based on type, length,
        and pattern type checks.
        Parameters:
            item (list[Any]): The item to check for suitability.
        Returns:
            bool: True if the item is suitable, False otherwise.
        """
        return (
            self.is_proper_type(item)
            and self.is_proper_length(item)
            and self.is_proper_pattern(item)
        )

    @staticmethod
    def is_proper_type(item: Iterable[Any]) -> bool:
        """
        Check if the passed argument is of type Iterable.
        Parameters:
            item (Iterable[Any]): The variable to be checked.
        Returns:
            bool: True if 'item' is an Iterable, False otherwise.
        """
        result = isinstance(item, Iterable)
        log.debug("Is proper type: %s", result)
        return result

    def is_proper_length(self, item: Iterable[Any]) -> bool:
        """
        Checks if the given 'item' has a length equal to the
        'number_of_items' attribute.
        Parameters:
            item (list[Any]): The list to check the length of.
        Returns:
            bool: True if 'item' length is equal to 'number_of_items',
                False otherwise.
        """
        if not isinstance(item, Sized):
            item = tuple(item)

        result = len(item) == self.number_of_items
        log.debug("Is proper length: %s", result)
        return result

    def append(self, item: Iterable[Any]):
        """
        Appends an item to the collection after conversion and
        suitability check.
        Parameters:
            item (list[Any]): A list of elements to be converted and appended.
        Raises:
            ValueError: If the item is not suitable for the collection.
        """
        item_to_append = self.convert_item_elements(item)
        if not self._is_item_suitable(item_to_append):
            raise ValueError("Item is not suitable for this collection.")
        super().append(item_to_append)

    def extend(self, iterable: Iterable[Iterable[Any]]):
        """
        Extends the collection by appending elements from the iterable.
        Parameters:
            iterable: An iterable of list items to append to the list.
        """
        for item in iterable:
            self.append(item)

    def insert(self, index: int, item: Iterable[Any]):
        """
        Inserts an item at a specified index if the item is suitable for
        this collection. Overrides the parent class insert method.
        Parameters:
            index (int): The index at which the item should be inserted.
            item: The item to insert into the collection.
        Raises:
            ValueError: If the item is not suitable for the collection.
        """
        if self._is_item_suitable(item):
            super().insert(index, item)
        else:
            raise ValueError("Item is not suitable for this collection.")

    def __setitem__(self, index: int, item: Iterable[Any]):
        """
        Overrides the `__setitem__` method to insert an item at a given
        index if the item is suitable for the collection.

        Parameters:
            index (int): The index at which the item should be inserted.
            item (any): The item to insert into the collection.

        Raises:
            ValueError: If the item is not suitable for the collection.
        """
        if self._is_item_suitable(item):
            super().__setitem__(index, item)
        else:
            raise ValueError("Item is not suitable for this collection.")

    @staticmethod
    def convert_item_elements(item: Iterable[Any]) -> tuple[Any, ...]:
        """
        Converts elements of a list to their respective data types.

        This static method takes a list of elements in a string format
        and converts each element to its actual data type (integers,
        booleans, or None). If the conversion is not applicable, it
        returns the element unchanged.

        Parameters:
            item (list[Any]): A list of elements to convert.

        Returns:
            list[Any]: A list with elements converted to their proper
                data types.
        """

        def convert_element(x: str) -> Any:
            """
            Converts a string to an integer, boolean, None, or keeps it as a string.
            Parameters:
                x (str): The string to convert.
            Returns:
                int: If 'x' is a digit.
                bool: If 'x' is 'true'/'True' or 'false'/'False'.
                None: If 'x' is an empty string.
                str: If 'x' does not match any of the above conditions.
            """
            if x.isdigit():
                return int(x)
            if x.lower() == "true":
                return True
            if x.lower() == "false":
                return False
            if x == "":
                return None
            return x

        return tuple(convert_element(x) for x in item)

    def is_proper_pattern(self, item: Iterable[Any]) -> bool:
        """
        Validates if each element in the input list matches a pattern
        of expected types. The pattern is defined by the 'self.pattern'
        attribute which contains types or tuples of types. None is
        considered a valid type and is replaced by 'type(None)'.

        Parameters:
            item (Iterable[Any]): The list of elements to validate against the
                pattern.

        Returns:
            bool: True if each element in the list matches the expected
                data type(s) from the pattern; False otherwise.
        """

        for types, value in zip(self.pattern, item):
            prepared_types = self.prepared_types(types)
            if not isinstance(value, prepared_types):
                log.debug(
                    f"{False} for item {item} in '{value}' "
                    f"with type '{type(value).__name__}': {prepared_types}"
                )
                return False
        log.debug("Is proper types for all elements: True")
        return True

    @staticmethod
    def prepared_types(expected_types):
        if not isinstance(expected_types, tuple):
            expected_types = (expected_types,)
        expected_types = tuple(
            type(None) if t is None else t for t in expected_types
        )
        return expected_types

    @classmethod
    def generate_containers(
        cls, table_properties_collection: Iterable[TableProperties]
    ) -> tuple[TableContainer, ...]:
        """
        Generates a list of TableContainer objects from the given
        collection of TableProperties.
        Parameters:
            table_properties_collection (list[TableProperties]): A list of TableProperties
                instances to be converted.
        Returns:
            list[TableContainer]: A list of TableContainer instances created
                from the provided TableProperties data.
        """
        return tuple(cls(data) for data in table_properties_collection)
