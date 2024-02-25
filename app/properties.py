# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

from __future__ import annotations

from typing import NamedTuple, Any


class ClassName:  # pylint: disable=too-few-public-methods
    authors = "Author"
    events = "LexEvent"
    types = "Type"
    words = "Words"
    word_spells = "WordSpell"
    definitions = "WordDefinition"
    settings = "Settings"
    syllables = "Syllable"

    def __iter__(self):
        return iter(
            (
                self.authors,
                self.events,
                self.types,
                self.words,
                self.word_spells,
                self.definitions,
                self.settings,
                self.syllables,
            )
        )


class TableProperties(NamedTuple):
    name: str
    pattern: list[Any]


DEFAULT_TABLE_PROPERTIES_COLLECTION = (
    TableProperties(
        ClassName.authors,
        [
            str,  # abbreviation
            str | None,  # full_name
            str | None,  # notes
        ],
    ),
    TableProperties(
        ClassName.events,
        [
            int,  # event_id
            str,  # name
            str,  # date
            str,  # definition
            str | None,  # annotation
            str | None,  # suffix
        ],
    ),
    TableProperties(
        ClassName.types,
        [
            str,  # type
            str,  # type_x
            str,  # group
            bool,  # parentable
            str | None,  # description
        ],
    ),
    TableProperties(
        ClassName.words,
        [
            int,  # old_id
            str,  # type.type
            str,  # type.type_x
            str | None,  # affixes
            str | None,  # match
            str | None,  # source
            str | None,  # year
            str | None,  # rank
            str | None,  # origin
            str | None,  # origin_x
            str | None,  # usedin
            int | None,  # tid_old
        ],
    ),
    TableProperties(
        ClassName.word_spells,
        [
            int,  # old_id
            str,  # name
            str,  # name.lower
            str,  # code_name
            int,  # event_start_id
            int,  # event_end_id
            str | None,  # origin_x
        ],
    ),
    TableProperties(
        ClassName.definitions,
        [
            int,  # source_word.old_id
            int,  # position
            str | None,  # usage
            str | None,  # grammar
            str,  # body
            str | None,  # main
            str | None,  # case_tags
        ],
    ),
    TableProperties(
        ClassName.settings,
        [
            str,  # date
            int,  # db_version
            int,  # last_word_id
            str,  # db_release
        ],
    ),
    TableProperties(
        ClassName.syllables,
        [
            str,  # name
            str,  # type
            bool,  # allowed
        ],
    ),
)
