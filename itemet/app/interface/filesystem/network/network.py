# -*- coding: <utf-8>
# internal
from . network_configuration import NetworkConfiguration
from . network_tables import NetworkTables


class FilesystemNetwork(object):
    """
    Class to handle all file system interactions to itemet database.
    """

    def __init__(self):
        self.config = NetworkConfiguration()
        self.tables = NetworkTables()

    def import_db_from_fs(self):
        self.config.add_net_config_to_db()
        self.tables.add_net_tables_to_db()

    def export_db_to_fs(self):
        self.tables.export_net_tables_to_fs()
        self.config.export_net_config_to_fs()


"""Main access point to file system item."""
fs_network = FilesystemNetwork()
