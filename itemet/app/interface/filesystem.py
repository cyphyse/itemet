# -*- coding: <utf-8>
# internal
from .. models.data.item import Item
# external
import os
import shutil
from sqlalchemy import event
# logging
import logging
logger = logging.getLogger(__name__)


PATH_ASSET = "asset"
PATH_TRASH = "trash"


class Filesystem(object):
    """
    Interface to filesystem.
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


class OrmFileSystemExtension(object):
    """
    Handler for ORM events.
    """

    def __init__(self, **kwargs):
        self.init_paths()

    def init_paths(self, **kwargs):
        """Initializes all paths."""
        asset = os.path.abspath(os.path.join(".", PATH_ASSET))
        asset = kwargs.get("asset", asset)
        trash = os.path.abspath(os.path.join(".", PATH_TRASH))
        trash = kwargs.get("trash", trash)
        self.fs = Filesystem(asset=asset, trash=trash)

    def on_create(self, name):
        """Triggers directory creation."""
        if isinstance(name, str):
            self.fs.create(name)

    def on_modify(self, src_name, dst_name):
        """Triggers renaming."""
        if isinstance(src_name, str) and isinstance(dst_name, str):
            self.fs.rename(src_name, dst_name)

    def on_delete(self, name):
        """Triggers remove."""
        if isinstance(name, str):
            self.fs.delete(name)


"""Main acces point to file system interface."""
orm_fs_ext = OrmFileSystemExtension()


@event.listens_for(Item, 'after_insert')
def receive_after_insert(mapper, connection, target):
    """Catches item creation and reroutes event."""
    orm_fs_ext.on_create(target.code)


@event.listens_for(Item.code, 'set')
def receive_set(target, value, oldvalue, initiator):
    """Catches item modification and reroutes event."""
    orm_fs_ext.on_modify(oldvalue, value)


@event.listens_for(Item, 'after_delete')
def receive_after_delete(mapper, connection, target):
    """Catches item delete and reroutes event."""
    orm_fs_ext.on_delete(target.code)


def main():
    """Small test for file system operations."""
    asset = os.path.abspath(os.path.join(".", PATH_ASSET))
    trash = os.path.abspath(os.path.join(".", PATH_TRASH))
    fs = Filesystem(asset=asset, trash=trash)
    fs.create("greate")
    fs.create("greate2")
    fs.rename("greate2", "greate3")
    fs.delete("greate")
    fs.clean()


if __name__ == '__main__':
    main()
