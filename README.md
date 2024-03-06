# Loglan Database Converter CLI Tool

[![Pylint App](https://github.com/torrua/loglan_convert/actions/workflows/pylint_app.yml/badge.svg)](https://github.com/torrua/loglan_convert/actions/workflows/pylint_app.yml)
[![BlackLint](https://github.com/torrua/loglan_convert/actions/workflows/black.yml/badge.svg)](https://github.com/torrua/loglan_convert/actions/workflows/black.yml)

## Supporting data types
postgres database, access mdb file, text files

## Usage
Run your terminal app with following command

```bash
python convert.py [-h] {postgres,access,text} from_path {postgres,access,text} to_path
```
##  Positional Arguments
```
  {postgres,access,text}    source type
  from_path                 source path
  {postgres,access,text}    destination type
  to_path                   destination path
```

## Options
```  
-h, --help            show this help message and exit
```

# Download data from GitHub source

Supporting data types
Empty Access database file, Filled Access database file, Text files

## Usage
Run your terminal app with following command
```
python download.py [-h] {text,empty-mdb,filled-mdb} url to-path
```

## Positional Arguments
```
  {text,empty-mdb,filled-mdb}   type of downloading
  url                           URL of the file to download
  to-path                       output directory for the downloaded file
```
## Options
```
  -h, --help                    show this help message and exit
```