# pylint: disable=missing-module-docstring, missing-class-docstring

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
        """
        Checks if a given path exists.
        Parameters:
            path (str): The path to check.
        Returns:
            bool: True if the path exists, False otherwise.
        Raises:
            ValueError: If no directory is provided.
            FileNotFoundError: If the directory is not found in the environment.
        """
        if path is None:
            raise ValueError("No Directory provided.")
        if os.path.exists(path):
            return True
        raise FileNotFoundError("Directory not found. Please check your environment.")

    @classmethod
    def check_files_in_directory(cls, directory: str) -> bool:
        """
        Check if all the files in the given directory exist.
        Parameters:
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
        """
        Returns a list of all the files in the directory.
        Returns:
            list[os.path]: A list of all the files in the directory.
        """
        return [
            os.path.join(self.path, file)
            for file in os.listdir(self.path)
            if file.endswith(f".{self.EXTENSION}")
        ]

    def path_by_name(self, name: str) -> str:
        """
        Returns the file path associated with the given name.
        Parameters:
            name (str): The name of the file without the file extension.
        Returns:
            str: The file path associated with the given name.
        Raises:
            FileNotFoundError: If the file with the given name is not found.
        """
        for file_path in self.files_paths:
            if file_path.endswith(f"{name}.{self.EXTENSION}"):
                return file_path
        raise FileNotFoundError(f"File '{name}' not found.")

    def content_by_name(self, name: str) -> str:
        """Reads the file from a given file name.
        Parameters:
            name (str): The name of the file.
        Returns:
            str: The content of the file.
        """
        with open(
            self.path_by_name(name), mode="r", encoding="utf-8"
        ) as file:
            return file.read()
