import argparse

from rich_argparse import RichHelpFormatter

from app.transfer import (
    storage_from_ac,
    storage_from_pg,
    storage_from_txt,
    storage_to_ac,
    storage_to_pg,
    storage_to_txt,
)


def generate_parser():

    supported_types = ["postgres", "access", "text"]

    parser = argparse.ArgumentParser(
        description="Database Converter CLI Tool", formatter_class=RichHelpFormatter
    )
    parser.add_argument(
        "--from-type", required=True, choices=supported_types, help="source type"
    )
    parser.add_argument("--from-path", required=True, help="source path")
    parser.add_argument(
        "--to-type", required=True, choices=supported_types, help="destination type"
    )
    parser.add_argument("--to-path", required=True, help="destination path")
    return parser


def db_converter(from_type, from_path, to_type, to_path):

    from_functions = {
        "access": storage_from_ac,
        "postgres": storage_from_pg,
        "text": storage_from_txt,
    }
    to_functions = {
        "access": storage_to_ac,
        "postgres": storage_to_pg,
        "text": storage_to_txt,
    }

    if from_type not in from_functions or to_type not in to_functions:
        raise ValueError("Invalid from_type or to_type")

    storage = from_functions.get(from_type)(from_path)
    to_functions.get(to_type)(to_path, storage)


if __name__ == "__main__":
    convert_parser = generate_parser()
    args = convert_parser.parse_args()
    db_converter(args.from_type, args.from_path, args.to_type, args.to_path)
