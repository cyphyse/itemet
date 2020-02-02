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

    def move(self, src_name, dst_name):
        src = self.get_asset_path(src_name)
        dst = self.get_asset_path(dst_name)
        self.hardmove(src, dst)

    def delete(self, name):
        """Moves directory to trash."""
        src = self.get_asset_path(name)
        dst = self.get_trash_path(name)
        self.hardmove(src, dst)

    def clean(self):
        shutil.rmtree(self.asset)
        shutil.rmtree(self.trash)


class ORMFilesystemEvents(object):
    """
    Interface to filesystem.
    """

    def __init__(self, **kwargs):
        self.init_paths()

    def init_paths(self, **kwargs):
        asset = os.path.abspath(os.path.join(".", PATH_ASSET))
        asset = kwargs.get("asset", asset)
        trash = os.path.abspath(os.path.join(".", PATH_TRASH))
        trash = kwargs.get("trash", trash)
        self.fs = Filesystem(asset=asset, trash=trash)

    def on_create(self, name):
        if isinstance(name, str):
            self.fs.create(name)

    def on_modify(self, src_name, dst_name):
        if isinstance(src_name, str) and isinstance(dst_name, str):
            self.fs.move(src_name, dst_name)

    def on_delete(self, name):
        if isinstance(name, str):
            self.fs.delete(name)


orm = ORMFilesystemEvents()


@event.listens_for(Item, 'after_insert')
def receive_after_insert(mapper, connection, target):
    orm.on_create(target.code)


@event.listens_for(Item.code, 'set')
def receive_set(target, value, oldvalue, initiator):
    orm.on_modify(oldvalue, value)


@event.listens_for(Item, 'after_delete')
def receive_after_delete(mapper, connection, target):
    orm.on_delete(target.code)


def main():
    """Small test."""
    asset = os.path.abspath(os.path.join(".", PATH_ASSET))
    trash = os.path.abspath(os.path.join(".", PATH_TRASH))
    fs = Filesystem(asset=asset, trash=trash)
    fs.create("greate")
    fs.create("greate2")
    fs.move("greate2", "greate3")
    fs.delete("greate")
    fs.clean()


if __name__ == '__main__':
    main()
