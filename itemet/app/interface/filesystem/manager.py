# -*- coding: <utf-8>
# internal
from ... import app, db
from ... entity.model.objects.item_model import Item
from .. plugins.trigger import plugintrigger
from . network.network import fs_network
from . storage.storage import fs_storage


class FilesystemManager(object):
    """
    Class to handle all file system interactions to itemet database.
    """

    def __init__(self):
        self.network = fs_network
        self.storage = fs_storage

    def import_db_from_fs(self):
        self.network.import_db_from_fs()

    def export_db_to_fs(self):
        self.network.export_db_to_fs()
        base_path = app.config['ITEMET'].get("path").get("itemet items")
        plugintrigger.on_event(base_path)

    def create_item_document(self, item_code):
        item = db.session.query(Item).filter_by(code=item_code).first()
        files = self.storage.doc.make(item)
        plugintrigger.on_event(files[0])
        plugintrigger.on_event(files[1])

"""Main access point to file system interface."""
fs_mngr = FilesystemManager()
