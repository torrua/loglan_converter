# Loglan Database Converter CLI Tool

[![Pylint App](https://github.com/torrua/loglan_convert/actions/workflows/pylint_app.yml/badge.svg)](https://github.com/torrua/loglan_convert/actions/workflows/pylint_app.yml)
[![BlackLint](https://github.com/torrua/loglan_convert/actions/workflows/black.yml/badge.svg)](https://github.com/torrua/loglan_convert/actions/workflows/black.yml)
![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability-percentage/torrua/loglan_converter?logo=Code%20Climate)

## Supporting data types
postgres database, access mdb file, prepared text files

## Usage
Run your terminal app with following command:

```bash
python convert.py [-h] {postgres, access, text} from_path {postgres, access, text} to_path
```
##  Positional Arguments
```
  {postgres, access, text}  source type
  from_path                 source path
  {postgres, access, text}  destination type
  to_path                   destination path
```

## Options
```  
-h, --help            show this help message and exit
```

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