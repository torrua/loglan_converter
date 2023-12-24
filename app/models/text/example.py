import os
from app.models.text.connector import TextConnector


if __name__ == "__main__":
    dir_path = os.getenv("TXT_DATABASE_URL")
    tc = TextConnector(dir_path)
    print(tc)
    print(tc.files_paths)
    print(tc.file_by_name("Author"))
