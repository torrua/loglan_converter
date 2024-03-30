"""
This module defines a class called TableContainer, which is a subclass of list.
It represents a collection of TableProperties objects and provides additional functionality.

Classes:
    TableContainer: A list subclass representing a collection of TableProperties.
"""

from __future__ import annotations

from typing import Any, Iterable, SupportsIndex, overload

from app.properties import TableProperties
from app.table_container_functions import (
    check_proper_pattern,
    prepared_types,
    convert_element,
)
from logger import log


class TableContainer(list):
    """
    A list subclass representing a collection of TableProperties.
    Methods:
        append_directly: Appends an item to the collection without conversion.
        extend_directly: Extends the collection without conversion.
    Properties:
        number_of_items: Property that returns the number of items in the 'pattern' attribute.
    """

    def __init__(self, table_properties: TableProperties):
        """
        Initializes the object with properties from a TableProperties instance.
        Parameters:
            table_properties (TableProperties): An instance of TableProperties
            containing order, name, and pattern attributes.
        """
        super().__init__()
        (
            self.name,
            self._pattern,
        ) = table_properties
        self.pattern = [prepared_types(types) for types in self._pattern]

    def __repr__(self):
        return f"{self.name}{self.__class__.__name__}({len(self)})"

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
        Checks if the given 'item' has a length equal to the 'number_of_items' attribute.
        Parameters:
            item (list[Any]): The list to check the length of.
        Returns:
            bool: True if 'item' length is equal to 'number_of_items',
                False otherwise.
        """
        result = len(tuple(item)) == len(self.pattern)
        log.debug("Is proper length: %s", result)
        return result

    def append(self, item: Iterable[Any]):
        """
        Appends an item to the collection after conversion and suitability check.
        Parameters:
            item (list[Any]): A list of elements to be converted and appended.
        Raises:
            ValueError: If the item is not suitable for the collection.
        """
        item_to_append = self.convert_item_elements(item)
        if not self._is_item_suitable(item_to_append):
            raise ValueError(
                f"Item of class '{self.name}' is not suitable for this collection."
            )
        super().append(item_to_append)

    def append_directly(self, item: Iterable[Any]):
        """
        Appends an item to the collection without conversion.
        Parameters:
            item (list[Any]): A list of elements to be appended.
        """
        super().append(item)

    def extend(self, iterable: Iterable[Iterable[Any]]):
        """
        Extends the collection by appending elements from the iterable.
        Parameters:
            iterable: An iterable of list items to append to the list.
        """
        for item in iterable:
            self.append(item)

    def extend_directly(self, iterable: Iterable[Iterable[Any]]):
        """
        Extends the collection without conversion.
        Parameters:
            iterable: An iterable of list items to append to the list.
        """
        super().extend(iterable)

    def insert(self, index: SupportsIndex, item: Iterable[Any]):
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

    def insert_directly(self, index: int, item: Iterable[Any]):
        """
        Inserts an item at a specified index. Overrides the parent class insert method.
        Parameters:
            index (int): The index at which the item should be inserted.
            item: The item to insert into the collection.
        """
        super().insert(index, item)

    @overload
    def __setitem__(self, index: SupportsIndex, item: Any) -> None: ...

    @overload
    def __setitem__(self, s: slice, items: Iterable[Any]) -> None: ...

    def __setitem__(
        self, index: SupportsIndex | slice, item: Any | Iterable[Any]
    ) -> None:
        """
        Set the value of an item in the object based on the given index.
        Parameters:
            index (SupportsIndex | slice): The index of the item to set.
            It can be an instance of SupportsIndex or a slice.
            item (Any | Iterable[Any]): The value to set for the item.
            It can be a single value or an iterable of values.
        Raises:
            IndexError: If the index is not an instance of SupportsIndex or slice.
        Returns:
            None: This function does not return anything.
        """
        if isinstance(index, slice):
            self._setitem_slice(index, item)
        elif isinstance(index, SupportsIndex):
            self._setitem_supports_index(index, item)
        else:
            raise IndexError("Index must be an SupportsIndex or slice.")

    def _setitem_slice(self, index, item):
        """
        Set the value of a slice in the collection.
        Parameters:
            index (slice): The slice to set the value for.
            item (Iterable): The iterable containing the items to set.
        Raises:
            TypeError: If the item is not an iterable.
            ValueError: If one or more items in the iterable are not suitable for the collection.
        Returns:
            None: This function does not return anything.
        """
        if not isinstance(item, Iterable):
            raise TypeError("When using a slice, the item should be an iterable.")
        # Ensure all items in the iterable are suitable for the collection
        if all(self._is_item_suitable(i) for i in item):
            super().__setitem__(index, item)
        else:
            raise ValueError("One or more items are not suitable for this collection.")

    def _setitem_supports_index(self, index, item):
        if not self._is_item_suitable(item):
            raise ValueError("Item is not suitable for this collection.")
        super().__setitem__(index, item)

    def convert_item_elements(self, item: Iterable[Any]) -> list[Any]:
        """
        Converts elements of a list to their respective data types. This static method takes a list
        of elements in a string format and converts each element to its actual data type (integers,
        booleans, or None). If the conversion is not applicable, it returns the element unchanged.
        Parameters:
            item (list[Any]): A list of elements to convert.
        Returns:
            list[Any]: A list with elements converted to their proper
                data types.
        """
        check_pairs = zip(item, self.pattern)
        return [convert_element(value, types) for value, types in check_pairs]

    def is_proper_pattern(self, item: Iterable[Any]) -> bool:
        """
        Validates if each element in the input list matches a pattern of expected types.
        The pattern is defined by the 'self.pattern' attribute which contains types or
        tuples of types. None is considered a valid type and is replaced by 'type(None)'.
        Parameters:
            item (Iterable[Any]): The list of elements to validate against the
                pattern.
        Returns:
            bool: True if each element in the list matches the expected
                data type(s) from the pattern; False otherwise.
        """
        return check_proper_pattern(item, self.pattern)

    @classmethod
    def generate_containers(
        cls, table_properties_collection: Iterable[TableProperties]
    ) -> tuple[TableContainer, ...]:
        """
        Generates a list of TableContainer objects from the given collection of TableProperties.
        Parameters:
            table_properties_collection (list[TableProperties]):
            A list of TableProperties instances to be converted.
        Returns:
            list[TableContainer]: A list of TableContainer instances created
                from the provided TableProperties data.
        """
        return tuple(cls(data) for data in table_properties_collection)
