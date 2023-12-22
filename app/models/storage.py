# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

from abc import ABC, abstractmethod
from typing import Type, Any

from logger import log


class BaseItemsCollection(list, ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    def length(self) -> int:
        return self._length()

    @classmethod
    def _length(cls) -> int:
        return len(cls._types_pattern())

    @property
    def types_pattern(self) -> list[Type | tuple[Type, ...]]:
        return self._types_pattern()

    @staticmethod
    @abstractmethod
    def _types_pattern() -> list[Type | tuple[Type, ...]]:
        pass

    @property
    def order(self) -> int:
        return self._order()

    @classmethod
    @abstractmethod
    def _order(cls) -> int:
        pass

    @classmethod
    @abstractmethod
    def _is_item_suitable(cls, item: list[str]) -> bool:
        item_to_append = cls.convert_item_elements(item)
        return (
            cls.is_proper_type(item_to_append)
            and cls.is_proper_length(item_to_append)
            and cls.check_types_by_pattern(item_to_append)
        )

    @staticmethod
    def is_proper_type(item: list[Any]) -> bool:
        result = isinstance(item, list)
        log.debug("Is proper type: %s", result)
        return result

    @classmethod
    def is_proper_length(cls, item: list[str]) -> bool:
        result = len(item) == cls._length()
        log.debug("Is proper length: %s", result)
        return result

    def append(self, item: list[str]):
        if not self._is_item_suitable(item):
            raise TypeError("Item is not suitable for this collection")
        item_to_append = self.convert_item_elements(item)
        super().append(item_to_append)

    @staticmethod
    def convert_item_elements(item: list[str]) -> list[Any]:
        def convert_element(x):
            if x.isdigit():
                return int(x)
            if x.lower() == "true":
                return True
            if x.lower() == "false":
                return False
            if x == "":
                return None
            return x

        return [convert_element(x) for x in item]

    @classmethod
    def check_types_by_pattern(cls, item: list[str]) -> bool:
        processed_pattern = []
        for expected_types in cls._types_pattern():
            if not isinstance(expected_types, tuple):
                expected_types = (expected_types,)
            expected_types = tuple(
                type(None) if t is None else t for t in expected_types
            )
            processed_pattern.append(expected_types)

        for expected_types, value in zip(processed_pattern, item):
            if not isinstance(value, expected_types):
                return False
        return True


class Author(BaseItemsCollection):
    @property
    def name(self) -> str:
        return "Author"

    @classmethod
    def _is_item_suitable(cls, item: list[str]) -> bool:
        return super()._is_item_suitable(item)

    @staticmethod
    def _types_pattern():
        # abbreviation, full_name, notes
        return [str, str | None, str | None]

    @classmethod
    def _order(cls) -> int:
        return 1


class Event(BaseItemsCollection):
    @property
    def name(self) -> str:
        return "LexEvent"

    @classmethod
    def _is_item_suitable(cls, item: list[str]) -> bool:
        return super()._is_item_suitable(item)

    @staticmethod
    def _types_pattern():
        # id, name, date, definition, annotation, suffix
        return [int, str, str, str, str | None, str | None]

    @classmethod
    def _order(cls) -> int:
        return 2


class WordType(BaseItemsCollection):
    @property
    def name(self) -> str:
        return "Type"

    @classmethod
    def _is_item_suitable(cls, item: list[str]) -> bool:
        return super()._is_item_suitable(item)

    @staticmethod
    def _types_pattern():
        # type, type_x, group, parentable, description
        return [str, str, str, bool, str | None]

    @classmethod
    def _order(cls) -> int:
        return 3


class Word(BaseItemsCollection):
    @property
    def name(self) -> str:
        return "Words"

    @classmethod
    def _is_item_suitable(cls, item: list[str]) -> bool:
        return super()._is_item_suitable(item)

    @staticmethod
    def _types_pattern():
        # old_id, type.type, type.type_x, affixes, match,
        # source, year, rank, origin, origin_x, usedin, tid_old
        return [
            int,
            str,
            str,
            str | None,
            str | None,
            str | None,
            str | None,
            str | None,
            str | None,
            str | None,
            str | None,
            int | None,
        ]

    @classmethod
    def _order(cls) -> int:
        return 4


class WordSpell(BaseItemsCollection):
    @property
    def name(self) -> str:
        return "WordSpell"

    @classmethod
    def _is_item_suitable(cls, item: list[str]) -> bool:
        return super()._is_item_suitable(item)

    @staticmethod
    def _types_pattern():
        # old_id, name, name.lower, code_name, event_start_id, event_end_id
        return [
            int,
            str,
            str,
            str,
            int,
            int,
            str | None,
        ]

    @classmethod
    def _order(cls) -> int:
        return 5


class Definition(BaseItemsCollection):
    @property
    def name(self) -> str:
        return "WordDefinition"

    @classmethod
    def _is_item_suitable(cls, item: list[str]) -> bool:
        return super()._is_item_suitable(item)

    @staticmethod
    def _types_pattern():
        # source_word.old_id, position, usage, grammar, body, main, case_tags
        return [
            int,
            int,
            str | None,
            str | None,
            str,
            str | None,
            str | None,
        ]

    @classmethod
    def _order(cls) -> int:
        return 6


class Settings(BaseItemsCollection):
    @property
    def name(self) -> str:
        return "Settings"

    @classmethod
    def _is_item_suitable(cls, item: list[str]) -> bool:
        return super()._is_item_suitable(item)

    @staticmethod
    def _types_pattern():
        # date, db_version, last_word_id, db_release
        return [str, int, int, str]  # TODO: add [0] as date

    @classmethod
    def _order(cls) -> int:
        return 7


class Syllable(BaseItemsCollection):
    @property
    def name(self) -> str:
        return "Syllable"

    @classmethod
    def _is_item_suitable(cls, item: list[str]) -> bool:
        return super()._is_item_suitable(item)

    @staticmethod
    def _types_pattern():
        # name, type, allowed
        return [str, str, bool | None]

    @classmethod
    def _order(cls) -> int:
        return 8


class Storage:
    def __repr__(self):
        return str(self.__dict__)

    def __init__(self):
        self.author: Author = Author()
        self.event: Event = Event()
        self.settings: Settings = Settings()
        self.syllable: Syllable = Syllable()
        self.word_type: WordType = WordType()
        self.word: Word = Word()
        self.word_spell: WordSpell = WordSpell()
        self.definition: Definition = Definition()


if __name__ == "__main__":
    all_models = [
        Author,
        Event,
        WordType,
        Word,
        WordSpell,
        Definition,
        Settings,
        Syllable,
    ]
    for model in all_models:
        print(model().name, model().types_pattern)
