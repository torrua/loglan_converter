# -*- coding: utf-8 -*-
"""
Module for check database data
"""

import re

from loglan_core import Syllable, Type, Definition, Word
from loglan_core.addons.definition_selector import DefinitionSelector
from loglan_core.addons.word_selector import WordSelector
from loglan_core.addons.word_sourcer import WordSourcer
from sqlalchemy import any_, select
from sqlalchemy.orm import Session

from logger import log


def check_tag_match(session: Session, extended_result: bool = False):
    """
    Determine the discrepancy between the declared tags
    and those actually specified in the Definition
    :param session: Database session
    :param extended_result: If True, returns an expanded dataset instead of a boolean
    :return: Boolean or tuple, depending on the extended_result variable
    """

    definitions = DefinitionSelector().filter(Definition.case_tags != "").all(session)
    for definition in definitions:
        pattern_case_tags = f"[{''.join(Definition.APPROVED_CASE_TAGS)}]"
        list_tags = re.findall(pattern_case_tags, definition.case_tags)
        list_body = [
            tag
            for tag in re.findall(r"\w+", definition.body)
            if tag in Definition.APPROVED_CASE_TAGS
        ]

        result = list_tags == list_body

        if result:
            continue

        if extended_result:
            # print(df.source_word.name, result, list_tags, list_body)
            if len(definition.source_word.definitions.all()) > 1 and not list_body:
                second = (
                    f"\n\t{definition.source_word.definitions[1].grammar}"
                    f" {definition.source_word.definitions[1].body}"
                )
            else:
                second = ""
            print(
                f"{definition.source_word.name},\n\t{definition.grammar}"
                f" {definition.body}{second} >< [{definition.case_tags}]\n"
            )
        else:
            print(definition.source_word.name, result)


def check_sources_primitives(session: Session):
    """
    :param session: Database session
    :return:
    """

    c_type = session.query(Type).filter(Type.type == "C-Prim").scalar()
    words = (
        session.query(Word)
        .filter(Word.type_id == c_type.id)
        .filter(~Word.origin.like("% | %"))
        .all()
    )
    _ = [print(word) for word in words]


def check_sources_prim_d(session: Session):
    """
    :param session: Database session
    :return:
    """

    d_type = session.query(Type).filter(Type.type == "D-Prim").first()
    words = session.query(Word).filter(Word.type_id == d_type.id).all()
    _ = [print(WordSourcer().get_sources_prim(word)) for word in words]


def check_complex_sources(session: Session):
    """
    :param session: Database session
    :return:
    """
    log.info("Start checking sources of Cpxes")
    cpx_ids_subquery = select(Type.id).where(Type.group == "Cpx").subquery()
    words = session.query(Word).filter(Word.type_id.in_(cpx_ids_subquery)).all()
    for word in words:
        log.debug("Checking word: %s", word.name)
        trigger = 0
        sources = WordSourcer().get_sources_cpx(word, as_str=True)
        for source in sources:
            if not session.query(Word).filter(Word.name == source).first():
                trigger = 1
                print(f"Word '{source}' is not in the Dictionary")
        if trigger:
            print(f"{word.id_old} |\t{word.name} |\t{word.origin} |\t{word.origin_x}")
    log.info("Finish checking sources of Cpxes")


def check_unintelligible_ccc(session: Session):
    """
    :param session: Database session
    :return:
    """
    log.info("Start checking unintelligible CCC")
    unintelligible_ccc_statement = select(Syllable.name).where(
        Syllable.type == "UnintelligibleCCC"
    )
    unintelligible_ccc = session.execute(unintelligible_ccc_statement).scalars().all()

    ccc_filter = Word.name.like(any_([f"%{ccc}%" for ccc in unintelligible_ccc]))
    words = session.execute(select(Word).filter(ccc_filter)).scalars().all()
    _ = [print(word.name) for word in words]
    log.info("Finish checking unintelligible CCC")


def get_list_of_lw_with_wrong_linguistic_formula(session: Session):
    """All LW should follow the formula (C)V(V).
    This function collect all LW that does not match it.
    :param session: Database session
    """

    words = WordSelector().by_type(type_="LW").all(session)
    print(len(words))
    pattern = r"^[bcdfghjklmnprstvz]{0,1}[aoeiu]{1}[aoeiu]{0,1}$"

    for word in words:
        res = bool(re.match(pattern, word.name.lower()))

        if not res:
            print(f"{word.id_old} {word.name}, {res}")

    print(
        len([word for word in words if not bool(re.match(pattern, word.name.lower()))])
    )
