# -*- coding: <utf-8>
# internal
from .... import db
from .... entity.model.objects.item_state_model import ItemState
from .... entity.model.objects.item_type_model import ItemType
from .... entity.model.objects.item_model import Item
from . network_configuration import NetworkConfiguration
from . network_tables import NetworkTables


class FilesystemNetwork(object):
    """
    Class to handle all file system interactions to itemet database.
    """

    def __init__(self):
        self.config = NetworkConfiguration()
        self.tables = NetworkTables()

    def clear_db(self):
        # delete all connections first TODO: this is maybe not the right place
        for item in db.session.query(Item).all():
            item.needs = []
        for type in db.session.query(ItemType).all():
            type.type_needs = []
            type.type_states = []
        db.session.commit()
        # then delete actual items
        db.session.query(Item).delete()
        db.session.query(ItemType).delete()
        db.session.query(ItemState).delete()
        db.session.commit()

    def import_db_from_fs(self):
        # TODO: this is maybe not the right place
        self.clear_db()
        self.config.add_net_config_to_db()
        self.tables.add_net_tables_to_db()

    def export_db_to_fs(self):
        self.tables.export_net_tables_to_fs()
        self.config.export_net_config_to_fs()


"""Main access point to file system item."""
fs_network = FilesystemNetwork()
