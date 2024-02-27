# Loglan Database Converter CLI Tool

[![Pylint App](https://github.com/torrua/loglan_convert/actions/workflows/pylint_app.yml/badge.svg)](https://github.com/torrua/loglan_convert/actions/workflows/pylint_app.yml)
[![BlackLint](https://github.com/torrua/loglan_convert/actions/workflows/black.yml/badge.svg)](https://github.com/torrua/loglan_convert/actions/workflows/black.yml)

# Supporting databases
postgres, access, text

# Usage
Run your terminal app with following command

```bash
python convert.py --from-type db_type --from-path FROM_PATH --to-type db_type --to-path TO_PATH
```
# Options
```
  -h, --help                                show this help message and exit
  --from-type   {postgres,access,text}      source type
  --from-path   FROM_PATH                   source path
  --to-type     {postgres,access,text}      destination type
  --to-path     TO_PATH                     destination path
```