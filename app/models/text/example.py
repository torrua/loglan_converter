# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import os

from app.models.text.connector import TextConnector
from app.properties import ClassName

if __name__ == "__main__":
    dir_path = os.getenv("TXT_DATABASE_URL")
    tc = TextConnector(dir_path)
    print(tc)
    print(tc.files_paths)
    print(tc.path_by_name(ClassName.authors))
    print(tc.content_by_name(ClassName.authors))
