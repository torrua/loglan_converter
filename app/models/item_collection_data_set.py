from __future__ import annotations

from typing import NamedTuple, Any


class ItemCollectionData(NamedTuple):
    order: int
    name: str
    pattern: list[Any]


default_item_collection_data = (
    ItemCollectionData(
        1,
        "Author",
        [
            str,  # abbreviation
            str | None,  # full_name
            str | None,  # notes
        ],
    ),
    ItemCollectionData(
        2,
        "LexEvent",
        [
            int,  # id
            str,  # name
            str,  # date
            str,  # definition
            str | None,  # annotation
            str | None,  # suffix
        ],
    ),
    ItemCollectionData(
        3,
        "Type",
        [
            str,  # type
            str,  # type_x
            str,  # group
            bool,  # parentable
            str | None,  # description
        ],
    ),
    ItemCollectionData(
        4,
        "Words",
        [
            int,  # old_id
            str,  # type.type
            str,  # type.type_x
            str | None,  # affixes
            str | None,  # match
            str | None,  # source
            int | None,  # year
            str | None,  # rank
            str | None,  # origin
            str | None,  # origin_x
            str | None,  # usedin
            int | None,  # tid_old
        ],
    ),
    ItemCollectionData(
        5,
        "WordSpell",
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
    ItemCollectionData(
        6,
        "WordDefinition",
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
    ItemCollectionData(
        7,
        "Settings",
        [
            str,  # date TODO: add as date
            int,  # db_version
            int,  # last_word_id
            str,  # db_release
        ],
    ),
    ItemCollectionData(
        8,
        "Syllable",
        [
            str,  # name
            str,  # type
            bool | None,  # allowed
        ],
    ),
)
