from interfaces.database_interface import DatabaseInterface


class AccessInterface(DatabaseInterface):

    def __init__(self, engine):
        pass

    def export_data(self):
        pass

    def import_data(self, data):
        pass
