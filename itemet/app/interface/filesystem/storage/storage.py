# -*- coding: <utf-8>
# internal
from . storage_directory import StorageDirectory
from . storage_document import StorageItemDocument


class FilesystemStorage(object):
    """
    Class to handle all file system interactions to itemet database.
    """

    def __init__(self):
        self.dir = StorageDirectory()
        self.doc = StorageItemDocument(self.dir)


"""Main access point to file system item."""
fs_storage = FilesystemStorage()
