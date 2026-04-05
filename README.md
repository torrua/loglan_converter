# Loglan Database Converter CLI Tool

[![Pylint App](https://github.com/torrua/loglan_convert/actions/workflows/pylint_app.yml/badge.svg)](https://github.com/torrua/loglan_convert/actions/workflows/pylint_app.yml)
[![BlackLint](https://github.com/torrua/loglan_convert/actions/workflows/black.yml/badge.svg)](https://github.com/torrua/loglan_convert/actions/workflows/black.yml)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability-percentage/torrua/loglan_converter?logo=Code%20Climate)

## Supported data types

PostgreSQL database, MS Access mdb file, prepared text files, SQLite database

## Usage

Run your terminal app with following command:

```bash
python convert.py [-h] {postgres, access, text, sqlite} from_path {postgres, access, text, sqlite} to_path
```

## Positional Arguments

```
  {postgres, access, text, sqlite}  source type
  from_path                         source path
  {postgres, access, text, sqlite}  destination type
  to_path                           destination path
```

## Options

```
  -h, --help            show this help message and exit
```

## Examples

```bash
# Export from MS Access to SQLite
python convert.py access "data/LoglanDictionary.mdb" sqlite "data/export.db"

# Export from PostgreSQL to text files
python convert.py postgres "postgresql://user:pass@localhost/db" text "data/text_output"

# Import text files into SQLite
python convert.py text "data/text_output/20260405132048" sqlite "data/import.db"

# Copy between SQLite databases
python convert.py sqlite "data/source.db" sqlite "data/destination.db"
```

## Configuration

Set database paths in `.env`:

```
LOD_DATABASE_URL=postgresql://postgres:password@localhost:5432/loglan_api
MDB_DATABASE_URL=C:\path\to\LoglanDictionary.mdb
TXT_DATABASE_URL=C:\path\to\data\text
SQLITE_DATABASE_EXPORT=C:\path\to\data\loglan_export.db

LOD_DATABASE_IMPORT=postgresql://postgres:password@localhost:5432/loglan_api
MDB_DATABASE_IMPORT=C:\path\to\LoglanDictionaryForImport.mdb
TXT_DATABASE_IMPORT=C:\path\to\data\text\text_import
SQLITE_DATABASE_IMPORT=C:\path\to\data\loglan_import.db
```

## Conversion matrix

| From \ To   | postgres | access | text | sqlite |
|-------------|----------|--------|------|--------|
| **postgres** | ✓        | ✓      | ✓    | ✓      |
| **access**   | ✓        | ✓      | ✓    | ✓      |
| **text**     | ✓        | ✓      | ✓    | ✓      |
| **sqlite**   | ✓        | ✓      | ✓    | ✓      |

# Download data from GitHub source

Supporting data types:

* empty access database file
* filled access database file
* filled text files

## Usage

Run your terminal app with following command:

```
python download.py [-h] {text, empty-mdb, filled-mdb} url to-path
```

## Positional Arguments

```
  {text, empty-mdb, filled-mdb} type of downloading
  url                           URL of the file to download
  to-path                       output directory for the downloaded file
```

## Options

```
  -h, --help                    show this help message and exit
```
