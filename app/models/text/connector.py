# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

import os

from app.models.storage.storage import Storage


class TextConnector:
    EXTENSION = "txt"

    def __init__(self, path: str):
        self.is_path(path)
        self.check_files_in_directory(path)
        self.path = path

    def __repr__(self):
        return f'{self.__class__.__name__}(path="{self.path}")'

    @staticmethod
    def is_path(path: str) -> bool:
        if path is None:
            raise ValueError("No Directory provided.")
        if os.path.exists(path):
            return True
        raise FileNotFoundError("Directory not found. Please check your environment.")

    @classmethod
    def check_files_in_directory(cls, directory: str) -> bool:
        """
        Check if all the files in the given directory exist.
        Args:
            directory (str): The directory to check for files.
        Returns:
            bool: True if all files exist, False otherwise.
        Raises:
            FileNotFoundError: If any of the files are missing.
        """
        files = os.listdir(directory)
        missing_files = [
            string
            for string in Storage().names
            if not any(file.endswith(f"{string}.{cls.EXTENSION}") for file in files)
        ]

        if missing_files:
            raise FileNotFoundError(f"Missing files: {', '.join(missing_files)}")
        return True

    @property
    def files_paths(self) -> list[os.path]:
        return [
            os.path.join(self.path, file)
            for file in os.listdir(self.path)
            if file.endswith(f".{self.EXTENSION}")
        ]

    def path_by_name(self, name: str) -> str:
        if name not in Storage().names:
            raise FileNotFoundError(f"File '{name}' not found.")
        for file_path in self.files_paths:
            if file_path.endswith(f"{name}.{self.EXTENSION}"):
                print(file_path)
                return file_path

    def file_by_name(self, name: str) -> str:
        with open(self.path_by_name(name), "r") as file:
            return file.read()
