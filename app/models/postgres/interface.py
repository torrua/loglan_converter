# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

from loglan_core import Author, Type, Word, Key, Definition, WordSelector
from loglan_core.addons.definition_selector import DefinitionSelector
from loglan_core.addons.exporter import Exporter
from loglan_core.addons.word_linker import WordLinker
from sqlalchemy import func, select

from app.database_interface import DatabaseInterface
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
log.level = logging.ERROR


class PostgresInterface(DatabaseInterface):
    def __init__(self, connector: PostgresDatabaseConnector):
        """
        Initialize the PostgresInterface object.
        """
        self.connector = connector

    @logging_time
    def export_data(self) -> Storage:
        s = Storage()
        with self.connector.session() as session:
            for container, class_ in zip(
                s.containers, self.connector.table_order.values()
            ):
                objects = session.query(class_).all()
                log.info("Exporting %s", class_.__name__)

                for obj in objects:
                    exp = Exporter.export(obj, self.SEPARATOR)
                    exported_object = exp.split(self.SEPARATOR)
                    container.append(exported_object)

                log.info("Exported %s %s items\n", len(container), class_.__name__)
        # TODO Implement direct exporting
        return s

    @logging_time
    def import_data(self, data: Storage) -> None:
        self.import_simple_classes(data)
        self.import_words(data)
        self.import_definitions(data, "en")
        self.add_keys("en")
        self.link_keys()
        self.link_authors(data)
        self.link_complexes(data)
        self.link_affixes(data)

    def import_simple_classes(self, data):
        for class_name in [
            ClassName.authors,
            ClassName.events,
            ClassName.types,
            ClassName.settings,
            ClassName.syllables,
        ]:
            with self.connector.session() as session:
                class_ = self.connector.table_order.get(class_name)
                log.info("Importing %s", class_.__name__)
                container = data.container_by_name(class_name)
                objects = [class_(*item) for item in container]
                session.bulk_save_objects(objects)
                session.commit()
                log.info("Imported %s %s items\n", len(container), class_.__name__)

    def import_words(self, data):
        class_ = self.connector.table_order.get(ClassName.words)
        log.info("Importing %s", class_.__name__)

        words = data.container_by_name(ClassName.words)
        spell = data.container_by_name(ClassName.word_spells)

        with self.connector.session() as session:
            types_data = session.query(Type.type, Type.id).all()
            types = dict((item.type, item.id) for item in types_data)

        data = get_word_data(words, types)
        names = get_word_names(spell)

        words = [
            Word(
                **{
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
            )
            for index in names.keys()
        ]

        words.sort(key=lambda x: x.name)

        with self.connector.session() as session:
            session.bulk_save_objects(words)
            session.commit()

        log.info("Imported %s %s items\n", len(words), class_.__name__)

    def import_definitions(self, data, language: str):
        definitions = data.container_by_name(ClassName.definitions)

        all_definitions = []
        with self.connector.session() as session:
            for item in definitions:
                words = (
                    session.execute(WordSelector().filter(Word.id_old == int(item[0])))
                    .scalars()
                    .all()
                )
                for word in words:
                    all_definitions.append(
                        Definition(
                            **{
                                "word_id": word.id,
                                "position": int(item[1]),
                                "usage": item[2],
                                "slots": get_grammar(item[3])["slots"],
                                "grammar_code": get_grammar(item[3])["code"],
                                "body": item[4],
                                "language": language,
                                "case_tags": item[6],
                            }
                        )
                    )
            session.bulk_save_objects(all_definitions)
            session.commit()

    @logging_time
    def add_keys(self, language: str):
        log.info(
            "Importing %s", Key.__name__
        )  # TODO Rewrite for getting language from definitions

        with self.connector.session() as session:
            bodies = session.query(func.string_agg(Definition.body, "@")).scalar()
            keys = extract_keys(bodies, language)
            session.bulk_save_objects(keys)
            session.commit()
        log.info("Imported %s %s items\n", len(keys), Key.__name__)

    @logging_time
    def link_keys(self):
        with self.connector.session() as session:
            for definition in DefinitionSelector().all(session):
                keys_str = get_unique_keys_strings(definition.body)
                keys_obj = (
                    session.execute(
                        select(Key)
                        .filter(Key.word.in_(keys_str))
                        .filter(Key.language == definition.language)
                    )
                    .scalars()
                    .all()
                )
                definition.keys_query.extend(keys_obj)
            session.commit()

    @logging_time
    def link_authors(self, data: Storage):
        authors_data = generate_authors_data(data)

        with self.connector.session() as session:
            all_authors = session.execute(select(Author)).scalars().all()
            author_by_abbr = dict(
                (author.abbreviation, author) for author in all_authors
            )

            for word in WordSelector().all(session):
                authors_abbrs = authors_data[word.id_old]
                authors = [author_by_abbr[abbr] for abbr in authors_abbrs]
                WordLinker.add_authors(word, authors)

            session.commit()

    @logging_time
    def link_complexes(self, data: Storage):
        index_used_in = 10
        words = get_source_data_by_index(data, index_used_in)
        self.link_words(words, generate_complex_children)

    @logging_time
    def link_affixes(self, data: Storage):
        index_affixes = 3
        words = get_source_data_by_index(data, index_affixes)
        self.link_words(words, generate_djifoa_children)

    def link_words(self, words, generate_children_func):
        with self.connector.session() as session:
            for w in words:
                stmt = WordSelector().filter(Word.id_old == int(w[0]))
                parents = session.execute(stmt).scalars().all()

                for parent in parents:
                    children = generate_children_func(w, session)
                    WordLinker.add_children(parent, children)
            session.commit()


if __name__ == "__main__":
    import os

    URI = os.environ.get("LOD_DATABASE_URL")
    pdc = PostgresDatabaseConnector(URI)
    pi = PostgresInterface(pdc)
    storage = pi.export_data()

    URI_IMPORT = os.environ.get("LOD_DATABASE_IMPORT")
    pdc_import = PostgresDatabaseConnector(URI_IMPORT)
    pdc_import.recreate_tables()
    pi_import = PostgresInterface(pdc_import)
    pi_import.import_data(storage)
