# -*- coding: <utf-8>
# internal
from .... import app
# external
import os
import shutil
# logging
import logging
logger = logging.getLogger(__name__)


PATH_ASSET = "asset"
PATH_TRASH = "trash"


class FilesystemOperations(object):
    """
    Class to provide basic filesystem operations.
    """

    def __init__(self, **kwargs):
        self.asset = kwargs.get("asset")
        self.trash = kwargs.get("trash")

    def get_asset_path(self, name, *other):
        """Returns asset path"""
        return os.path.join(self.asset, name, *other)

    def get_trash_path(self, name, *other):
        """Returns trash path"""
        return os.path.join(self.trash, name, *other)

    def hardmove(self, src, dst):
        """
        Moves a directory.
        WARNING: Deletes target directory if it exists before.
        """
        if src == dst:
            return
        if not os.path.exists(src):
            return
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst, symlinks=False, ignore=None)
        shutil.rmtree(src)

    def create(self, name):
        """Creates asser directory."""
        dst = self.get_asset_path(name)
        if not os.path.exists(dst):
            os.makedirs(dst)

    def rename(self, src_name, dst_name):
        """Renames a asset directory."""
        src = self.get_asset_path(src_name)
        dst = self.get_asset_path(dst_name)
        self.hardmove(src, dst)

    def delete(self, name):
        """Moves asset directory to trash."""
        src = self.get_asset_path(name)
        dst = self.get_trash_path(name)
        self.hardmove(src, dst)

    def clean(self):
        """Removes all data. WARNING: Only for testing."""
        shutil.rmtree(self.asset)
        shutil.rmtree(self.trash)


class OrmFilesystemEvents(FilesystemOperations):
    """
    Class to handl ORM events.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_paths()

    def init_paths(self, **kwargs):
        """Initializes all paths."""
        asset = os.path.abspath(os.path.join(".", PATH_ASSET))
        self.asset = kwargs.get("asset", asset)
        trash = os.path.abspath(os.path.join(".", PATH_TRASH))
        self.trash = kwargs.get("trash", trash)

    def on_create(self, name):
        """Triggers directory creation."""
        if isinstance(name, str):
            self.create(name)

    def on_modify(self, src_name, dst_name):
        """Triggers renaming."""
        if isinstance(src_name, str) and isinstance(dst_name, str):
            self.rename(src_name, dst_name)

    def on_delete(self, name):
        """Triggers remove."""
        if isinstance(name, str):
            self.delete(name)

    def get_link(self, item_code, *args):
        filepath = self.get_asset_path(item_code, *args)
        p = app.config['ITEMET'].get("path").get("itemet db")
        link = filepath.replace(p, "/files")
        return link



class StorageDirectory(OrmFilesystemEvents):
    """
    Top class for common naming.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



def main():
    """Small test for file system operations."""
    asset = os.path.abspath(os.path.join(".", PATH_ASSET))
    trash = os.path.abspath(os.path.join(".", PATH_TRASH))
    fs = FilesystemOperations(asset=asset, trash=trash)
    fs.create("greate")
    fs.create("greate2")
    fs.rename("greate2", "greate3")
    fs.delete("greate")
    fs.clean()


if __name__ == '__main__':
    main()
