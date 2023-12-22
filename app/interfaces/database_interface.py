from abc import ABC, abstractmethod


class DatabaseInterface(ABC):

    @abstractmethod
    def export_data(self):
        pass

    @abstractmethod
    def import_data(self, data):
        pass
