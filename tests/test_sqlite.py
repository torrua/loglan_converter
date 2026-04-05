"""Tests for SQLite connector, interface, and wiring."""
import os
import tempfile
import pytest

from app.connector import DatabaseConnector
from app.interface import DatabaseInterface
from app.properties import ClassName
from app.storage import Storage


class TestSQLiteDatabaseConnector:
    """Tests for SQLiteDatabaseConnector."""

    def test_import_connector(self):
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        assert SQLiteDatabaseConnector is not None

    def test_connector_is_database_connector_subclass(self):
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        assert issubclass(SQLiteDatabaseConnector, DatabaseConnector)

    def test_instantiate_with_memory(self):
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        conn = SQLiteDatabaseConnector(":memory:")
        assert conn.path == ":memory:"
        assert conn.engine is not None

    def test_table_order_has_8_mappings(self):
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        conn = SQLiteDatabaseConnector(":memory:")
        assert len(conn.table_order) == 8
        assert ClassName.authors in conn.table_order
        assert ClassName.events in conn.table_order
        assert ClassName.types in conn.table_order
        assert ClassName.words in conn.table_order
        assert ClassName.word_spells in conn.table_order
        assert ClassName.definitions in conn.table_order
        assert ClassName.settings in conn.table_order
        assert ClassName.syllables in conn.table_order

    def test_session_returns_session(self):
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        conn = SQLiteDatabaseConnector(":memory:")
        session = conn.session
        assert session is not None

    def test_is_path_validates_memory(self):
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        assert SQLiteDatabaseConnector.is_path(":memory:") is True

    def test_is_path_validates_db_extension(self):
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        assert SQLiteDatabaseConnector.is_path("test.db") is True

    def test_is_path_validates_sqlite_extension(self):
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        assert SQLiteDatabaseConnector.is_path("test.sqlite") is True

    def test_is_path_rejects_empty(self):
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        with pytest.raises(ValueError, match="No SQLite path"):
            SQLiteDatabaseConnector.is_path("")

    def test_is_path_rejects_no_extension(self):
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        with pytest.raises(ValueError, match="Invalid SQLite path"):
            SQLiteDatabaseConnector.is_path("test.txt")

    def test_is_path_rejects_postgres_uri(self):
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        with pytest.raises(ValueError, match="Invalid SQLite path"):
            SQLiteDatabaseConnector.is_path("postgresql://localhost/db")

    def test_recreate_tables_creates_tables(self):
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        from sqlalchemy import inspect
        conn = SQLiteDatabaseConnector(":memory:", importing=True)
        inspector = inspect(conn.engine)
        tables = inspector.get_table_names()
        assert len(tables) > 0

    def test_get_engine_uses_sqlite_prefix(self):
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        engine = SQLiteDatabaseConnector.get_engine(":memory:")
        assert "sqlite" in str(engine.url)


class TestSQLiteInterface:
    """Tests for SQLiteInterface."""

    def test_import_interface(self):
        from app.models.sqlite.interface import SQLiteInterface
        assert SQLiteInterface is not None

    def test_interface_is_database_interface_subclass(self):
        from app.models.sqlite.interface import SQLiteInterface
        assert issubclass(SQLiteInterface, DatabaseInterface)

    def test_instantiate_interface(self):
        from app.models.sqlite.interface import SQLiteInterface
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        conn = SQLiteDatabaseConnector(":memory:")
        iface = SQLiteInterface(conn)
        assert iface.connector is conn

    def test_has_export_data_method(self):
        from app.models.sqlite.interface import SQLiteInterface
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        conn = SQLiteDatabaseConnector(":memory:", importing=True)
        iface = SQLiteInterface(conn)
        assert hasattr(iface, "export_data")
        assert callable(iface.export_data)

    def test_has_import_data_method(self):
        from app.models.sqlite.interface import SQLiteInterface
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        conn = SQLiteDatabaseConnector(":memory:", importing=True)
        iface = SQLiteInterface(conn)
        assert hasattr(iface, "import_data")
        assert callable(iface.import_data)

    def test_has_all_import_helper_methods(self):
        from app.models.sqlite.interface import SQLiteInterface
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        conn = SQLiteDatabaseConnector(":memory:", importing=True)
        iface = SQLiteInterface(conn)
        for method in [
            "import_simple_classes",
            "import_words",
            "import_definitions",
            "add_keys",
            "link_keys",
            "link_authors",
            "link_complexes",
            "link_affixes",
        ]:
            assert hasattr(iface, method)

    def test_export_data_returns_storage(self):
        from app.models.sqlite.interface import SQLiteInterface
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        conn = SQLiteDatabaseConnector(":memory:", importing=True)
        iface = SQLiteInterface(conn)
        result = iface.export_data()
        assert isinstance(result, Storage)

    def test_import_data_with_empty_storage(self):
        from app.models.sqlite.interface import SQLiteInterface
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        conn = SQLiteDatabaseConnector(":memory:", importing=True)
        iface = SQLiteInterface(conn)
        storage = Storage()
        iface.import_data(storage)

    def test_roundtrip_import_export(self):
        from app.models.sqlite.interface import SQLiteInterface
        from app.models.sqlite.connector import SQLiteDatabaseConnector
        from loglan_core import Author, Type, Syllable

        conn = SQLiteDatabaseConnector(":memory:", importing=True)
        iface = SQLiteInterface(conn)

        with conn.session as session:
            session.add(Author("TST", "Test Author", None))
            session.add(Type("Tst", "Test", "TestGroup", False, None))
            session.add(Syllable("ba", "CV", True))
            session.commit()

        exported = iface.export_data()
        assert exported is not None

        author_container = exported.container_by_name(ClassName.authors)
        assert len(author_container) > 0


class TestTransferWiring:
    """Tests for transfer.py SQLite functions."""

    def test_import_storage_from_sqlite(self):
        from app.transfer import storage_from_sqlite
        assert callable(storage_from_sqlite)

    def test_import_storage_to_sqlite(self):
        from app.transfer import storage_to_sqlite
        assert callable(storage_to_sqlite)

    def test_storage_to_sqlite_with_empty_storage(self, tmp_path):
        from app.transfer import storage_to_sqlite
        from app.storage import Storage
        db_path = str(tmp_path / "test.db")
        storage = Storage()
        storage_to_sqlite(db_path, storage)
        assert os.path.exists(db_path)


class TestCLIWiring:
    """Tests for convert.py SQLite CLI support."""

    def test_sqlite_in_supported_types(self):
        from convert import generate_parser
        parser = generate_parser()
        action = None
        for a in parser._actions:
            if a.dest == "from_type":
                action = a
                break
        assert action is not None
        assert "sqlite" in action.choices

    def test_all_four_types_in_cli(self):
        from convert import generate_parser
        parser = generate_parser()
        for action in parser._actions:
            if action.dest in ("from_type", "to_type"):
                assert set(action.choices) == {"postgres", "access", "text", "sqlite"}


class TestEnvConfig:
    """Tests for .env SQLite variables."""

    def test_env_has_sqlite_export(self):
        env = self._read_env()
        assert "SQLITE_DATABASE_EXPORT" in env

    def test_env_has_sqlite_import(self):
        env = self._read_env()
        assert "SQLITE_DATABASE_IMPORT" in env

    def test_sqlite_export_path_ends_with_db(self):
        env = self._read_env()
        assert env["SQLITE_DATABASE_EXPORT"].endswith(".db")

    def test_sqlite_import_path_ends_with_db(self):
        env = self._read_env()
        assert env["SQLITE_DATABASE_IMPORT"].endswith(".db")

    @staticmethod
    def _read_env():
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        result = {}
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    result[key.strip()] = value.strip()
        return result


class TestSQLiteSpecificSQL:
    """Tests that SQLite-specific SQL functions work (not PostgreSQL-only)."""

    def test_group_concat_in_add_keys(self):
        """Verify add_keys uses group_concat (SQLite) not string_agg (PostgreSQL)."""
        import inspect
        from app.models.sqlite.interface import SQLiteInterface
        source = inspect.getsource(SQLiteInterface.add_keys)
        assert "group_concat" in source
        assert "string_agg" not in source
