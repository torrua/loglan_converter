# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from __future__ import annotations

import re
from datetime import datetime

from loglan_core import Word, WordSelector

from app.properties import ClassName
from app.storage import Storage


def extract_keys(bodies: str, language: str) -> list[dict]:
    keys = get_unique_keys_strings(bodies)
    return [{"word": key, "language": language} for key in keys]


def get_unique_keys_strings(text: str) -> list[str]:
    key_pattern = r"(?<=\«)(.+?)(?=\»)"
    all_keys = re.findall(key_pattern, text)
    return sorted(set(all_keys))


def get_grammar(str_grammar: str) -> dict:
    slots = re.search(r"\d", str_grammar)
    code = re.search(r"\D+", str_grammar)

    return {
        "slots": int(slots.group(0)) if slots else None,
        "code": code.group(0) if code else "",
    }


def get_year(str_date: str) -> dict:
    date_year = str_date.split(" ", 1)
    return {
        "year": datetime.strptime(date_year[0], "%Y").date(),
        "notes": date_year[1] if len(date_year) > 1 else None,
    }


def get_rank(str_rank: str) -> dict:
    if not str_rank:
        return {"rank": None, "notes": None}

    rank_data = str_rank.split(" ", 1)
    return {
        "rank": rank_data[0],
        "notes": rank_data[1] if len(rank_data) > 1 else None,
    }


def get_author(str_author) -> dict:
    author_data = str_author.split(" ", 1)
    return {
        "author": author_data[0],
        "notes": author_data[1] if len(author_data) > 1 else None,
    }


def get_notes(item: list) -> dict | None:
    str_notes = {
        "author": get_author(item[5]).get("notes"),
        "year": get_year(item[6]).get("notes"),
        "rank": get_rank(item[7]).get("notes"),
    }
    return {k: v for k, v in str_notes.items() if v} or None


def get_word_names(spell):
    dict_of_word_names = {
        (index, int(item[0])): {
            "name": item[1],
            "id_old": int(item[0]),
            "event_start_id": int(item[4]),
            "event_end_id": int(item[5]) if int(item[5]) < 9999 else None,
        }
        for index, item in enumerate(spell)
    }
    return dict_of_word_names


def get_word_data(words, types):
    dict_of_word_data = {
        item[0]: {
            "authors": get_author(item[5]).get("author"),
            "type_id": types.get(item[1]),
            "origin": item[8],
            "origin_x": item[9],
            "id_old": int(item[0]),
            "match": item[4],
            "rank": get_rank(item[7]).get("rank"),
            "year": get_year(item[6]).get("year"),
            "tid_old": int(item[11]) if item[11] else None,
            "notes": get_notes(item),
        }
        for item in words
    }
    return dict_of_word_data


def get_elements_from_str(set_as_str: str, separator: str) -> list:
    return [element.strip() for element in set_as_str.split(separator)]


def get_source_data_by_index(data: Storage, index: int) -> list:
    words = [w for w in data.container_by_name(ClassName.words) if w[index]]
    return words


def generate_complex_children(w: list, session):
    child_names = get_elements_from_str(w[10], separator=" | ")
    stmt = WordSelector().filter(Word.name.in_(child_names))
    children = list(session.execute(stmt).scalars().all())
    return children


def generate_djifoa_children(w: list, session):
    djifoa = get_elements_from_str(w[3], separator=" ")
    djifoa_with_hyphen = [f"{df}-" for df in djifoa]
    all_djifoa = djifoa + djifoa_with_hyphen
    stmt = WordSelector().by_type(type_="Afx").filter(Word.name.in_(all_djifoa))
    children = list(session.execute(stmt).scalars().all())
    return children


def generate_authors_data(data: Storage) -> dict:
    return {
        int(w[0]): w[5].split(" ", 1)[0].split("/")
        for w in data.container_by_name(ClassName.words)
    }
