"""
This module contains functions that are used in the TableContainer class.
"""
from __future__ import annotations

from typing import Iterable, Any, Type, get_args

from logger import log


def check_proper_pattern(item: Iterable[Any], pattern: list) -> bool:
    """
    Validates if each element in the input list matches a pattern
    of expected types. The pattern is defined by the 'self.pattern'
    attribute which contains types or tuples of types. None is
    considered a valid type and is replaced by 'type(None)'.

    Parameters:
        item (Iterable[Any]): The list of elements to validate against the
            pattern.
        pattern (list): The expected types for each element in the list.
    Returns:
        bool: True if each element in the list matches the expected
            data type(s) from the pattern; False otherwise.
    """

    for types, value in zip(pattern, item):
        if not isinstance(value, types):
            log.debug(
                "False for item %s in '%s' with type '%s': %s",
                item,
                value,
                type(value).__name__,
                *types,
            )
            return False
    log.debug("Is proper types for all elements: True")
    return True


def prepared_types(actual_types: Type | tuple[Type, ...]) -> tuple[Type, ...]:
    """
    Prepares the expected types for a function.

    Parameters:
        actual_types (Union[type, Tuple[type]]): The expected types for the function.
            If a single type is provided, it will be converted to a tuple.
            If None is provided, the type will be converted to type(None).
    Returns:
        tuple[Type]: The prepared expected types.
    """
    args = get_args(actual_types)
    expected_types = args or (actual_types,)
    expected_types = tuple(type(None) if t is None else t for t in expected_types)
    return expected_types


def convert_element(value, types) -> Any:
    """
    Converts the given `value` to the appropriate data type
    based on the provided `types`.

    Parameters:
        value: The value to be converted.
        types: A list of data types to check against.

    Returns:
        The converted value if a matching data type is found.
        None if the `value` is empty or None.
        The original `value` if no matching data type is found.
    """

    if is_none(value, types):
        return None
    if is_int(value, types):
        return int(str(value))
    if bool in types:
        return convert_boolean(value)
    return value


def convert_boolean(value) -> bool:
    """
    Convert a string representation of a boolean to a boolean value.

    Parameters:
        value (str): The string representation of the boolean value.

    Returns:
        bool: The boolean value.

    Raises:
        ValueError: If the input value is not a valid boolean string.
    """
    if str(value).lower() == "true":
        return True
    if str(value).lower() == "false":
        return False
    raise ValueError(f"Invalid boolean value: {value}")


def is_none(value, types) -> bool:
    """
    Check if the given value is None and matches any of the specified types.

    Parameters:
        value (Any): The value to check.
        types (Tuple[Type, ...]): The types to compare against.

    Returns:
        bool: True if the value is None and matches any of the specified types, False otherwise.
    """
    return type(None) in types and not value


def is_int(value, types) -> bool:
    """
    Check if a value is an integer and belongs to a specific set of types.

    Parameters:
        value (Any): The value to check.
        types (Set[Type]): The set of types to check against.

    Returns:
        bool: True if the value is an integer and belongs to the specified types, False otherwise.
    """
    return int in types and str(value).isdigit()
