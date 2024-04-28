# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring
from collections import defaultdict

from loglan_core import Author, Type, Word, Key, Definition, WordSelector, WordSpell
from loglan_core.addons.definition_selector import DefinitionSelector
from loglan_core.addons.exporter import Exporter
from loglan_core.addons.word_linker import WordLinker
from sqlalchemy import func, select
from sqlalchemy.dialects import postgresql

from app.interface import DatabaseInterface
from app.models.postgres.connector import PostgresDatabaseConnector
from app.models.postgres.functions import (
    extract_keys,
    get_grammar,
    get_word_names,
    get_word_data,
    get_unique_keys_strings,
    get_source_data_by_index,
    generate_complex_children,
    generate_djifoa_children,
    generate_authors_data,
)
from app.properties import ClassName
from app.storage import Storage
from logger import logging, logging_time

log = logging.getLogger(__name__)
log.level = logging.INFO


class PostgresInterface(DatabaseInterface):
    def __init__(self, connector: PostgresDatabaseConnector):
        """
        Initialize the PostgresInterface object.
        """
        self.connector = connector

    @logging_time
    def export_data(self) -> Storage:
        return self.default_export(self.connector, self.get_data_from_objects)

    def get_data_from_objects(self, objects):
        return [
            Exporter.export(obj, self.SEPARATOR).split(self.SEPARATOR)
            for obj in objects
        ]

    @logging_time
    def import_data(self, data: Storage) -> None:
        self.import_simple_classes(data)
        self.import_words(data)
        self.import_definitions(data, "en")
        self.add_keys()
        self.link_keys()
        self.link_authors(data)
        self.link_complexes(data)
        self.link_affixes(data)

    @logging_time
    def import_simple_classes(self, data):
        for class_name in [
            ClassName.authors,
            ClassName.events,
            ClassName.types,
            ClassName.settings,
            ClassName.syllables,
        ]:
            with self.connector.session as session:
                class_ = self.connector.table_order.get(class_name)
                log.info("Importing %s", class_.__name__)
                container = data.container_by_name(class_name)
                objects = [class_(*item).__dict__ for item in container]
                session.execute(postgresql.insert(class_), objects)
                session.commit()
                log.info("Imported %s %s items\n", len(container), class_.__name__)

    @logging_time
    def import_words(self, data):
        class_ = self.connector.table_order.get(ClassName.words)

        log.info("Importing %s", class_.__name__)
        words = data.container_by_name(ClassName.words)

        log.info("Importing %s", WordSpell.__name__)
        spell = data.container_by_name(ClassName.word_spells)

        with self.connector.session as session:
            log.info("Getting %s for words", Type.__name__)
            types_data = session.query(Type.type, Type.id).all()
            types = dict((item.type, item.id) for item in types_data)

        data = get_word_data(words, types)
        names = get_word_names(spell)
        log.info("Generating list of %s", class_.__name__)
        words = [
            {
                "name": names.get(index).get("name"),
                "event_start_id": names.get(index).get("event_start_id"),
                "event_end_id": names.get(index).get("event_end_id"),
                "id_old": data.get(index[1]).get("id_old"),
                "origin": data.get(index[1]).get("origin"),
                "origin_x": data.get(index[1]).get("origin_x"),
                "type_id": data.get(index[1]).get("type_id"),
                "match": data.get(index[1]).get("match"),
                "rank": data.get(index[1]).get("rank"),
                "year": data.get(index[1]).get("year"),
                "notes": data.get(index[1]).get("notes"),
                "tid_old": data.get(index[1]).get("tid_old"),
            }
            for index in names.keys()
        ]
        log.info("Sorting list of %s", class_.__name__)
        words.sort(key=lambda x: x["name"])

        with self.connector.session as session:
            log.info("Saving list of %s to database", class_.__name__)
            session.execute(postgresql.insert(class_), words)
            session.commit()

        log.info("Imported %s %s items\n", len(words), class_.__name__)

    def _generate_word_id_name_dict(self) -> dict[int, list[tuple[int, str]]]:
        """
        Generates a dictionary mapping old word IDs to lists of tuples
        containing new word IDs and names.

        Returns:
            A dictionary where the keys are old word IDs and the values
            are lists of tuples with new word IDs and names.
        """
        with self.connector.session as session:
            words = session.query(Word.id_old, Word.id, Word.name).all()

        result_dict = defaultdict(list)

        for id_old, id_new, name in words:
            result_dict[id_old].append((id_new, name))

        return result_dict

    @logging_time
    def import_definitions(self, data, language: str):
        log.info("Importing %s", Definition.__name__)
        definitions = data.container_by_name(ClassName.definitions)

        all_definitions = []
        words = self._generate_word_id_name_dict()

        with self.connector.session as session:
            for index, item in enumerate(definitions, 1):
                words_of_definition = words.get(int(item[0]))
                for word in words_of_definition:
                    wid, name = word
                    all_definitions.append(
                        {
                            "word_id": wid,
                            "position": int(item[1]),
                            "usage": item[2],
                            "slots": get_grammar(item[3]).get("slots"),
                            "grammar_code": get_grammar(item[3]).get("code"),
                            "body": item[4],
                            "language": language,
                            "case_tags": item[6],
                        }
                    )
            session.execute(postgresql.insert(Definition), all_definitions)
            session.commit()

    @logging_time
    def add_keys(self):
        log.info("Importing %s", Key.__name__)
        with self.connector.session as session:
            languages = (
                session.execute(select(Definition.language.distinct())).scalars().all()
            )
            for language in languages:
                bodies = (
                    session.query(func.string_agg(Definition.body, self.SEPARATOR))
                    .filter(Definition.language == language)
                    .scalar()
                )
                keys = extract_keys(bodies, language)
                session.execute(postgresql.insert(Key), keys)
            session.commit()
        log.info("Imported %s %s items\n", len(keys), Key.__name__)

    @logging_time
    def link_keys(self):
        log.info("Linking %s", Key.__name__)
        with self.connector.session as session:
            languages = (
                session.execute(select(Definition.language.distinct())).scalars().all()
            )
            for language in languages:
                keys = session.execute(
                    select(Key.word, Key).filter(Key.language == language)
                ).all()
                keys = dict(keys)
                definitions = DefinitionSelector().by_language(language).all(session)

                for definition in definitions:
                    keys_str = get_unique_keys_strings(definition.body)
                    keys_obj = [keys.get(key) for key in keys_str]
                    definition.keys_query.extend(keys_obj)
            session.commit()

    @logging_time
    def link_authors(self, data: Storage):
        log.info("Linking %s", Author.__name__)
        authors_data = generate_authors_data(data)

        with self.connector.session as session:
            all_authors = session.execute(select(Author)).scalars().all()
            author_by_abbr = dict(
                (author.abbreviation, author) for author in all_authors
            )

            for word in WordSelector().all(session):
                authors_abbrs = authors_data[word.id_old]
                authors = [author_by_abbr[abbr] for abbr in authors_abbrs]
                word.authors_query.extend(authors)

            session.commit()

    @logging_time
    def link_complexes(self, data: Storage):
        log.info("Linking Complexes")
        index_used_in = 10
        words = get_source_data_by_index(data, index_used_in)
        self.link_words(words, generate_complex_children)

    @logging_time
    def link_affixes(self, data: Storage):
        log.info("Linking Affixes")
        index_affixes = 3
        words = get_source_data_by_index(data, index_affixes)
        self.link_words(words, generate_djifoa_children)

    def link_words(self, words, generate_children_func):
        with self.connector.session as session:
            for w in words:
                stmt = WordSelector().filter(Word.id_old == int(w[0]))
                parents = session.execute(stmt).scalars().all()

                for parent in parents:
                    children = generate_children_func(w, session)
                    WordLinker.add_children(parent, children)
            session.commit()
