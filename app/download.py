from pathlib import Path
from properties import ClassName
import os
import urllib.request


def download_txt_to_import(output_directory: str):
    """
    Downloads RAW text files from GitHub repository
    :return:
    """

    Path(output_directory).mkdir(parents=True, exist_ok=True)
    files = [
        f"https://raw.githubusercontent.com/torrua/LOD/master/tables/{name}.txt"
        for name in ClassName()
    ]

    for file in files:
        download_file(file, output_directory)


def download_file(source, output_directory: str):
    filename = os.path.basename(source)
    urllib.request.urlretrieve(source, f"{output_directory}{filename}")


def download_mdb_filled(output_directory: str):
    """
    Downloads filled mdb file from GitHub repository
    :return:
    """
    download_file(
        "https://github.com/torrua/LOD/raw/master/source/LoglanDictionary.mdb",
        output_directory,
    )


def download_mdb_empty(output_directory: str):
    """
    Downloads empty mdb file (template) from GitHub repository
    :return:
    """
    download_file(
        "https://github.com/torrua/LOD/raw/master/source/LoglanDictionaryTemplate.mdb",
        output_directory,
    )
