# -*- coding: <utf-8>
# internal
from . filesystem.manager import fs_mngr
from .. entity.model.objects.item_model import Item
# external
from sqlalchemy import event


@event.listens_for(Item, 'after_insert')
def receive_after_insert(mapper, connection, target):
    """Catches item creation and reroutes event."""
    fs_mngr.storage.dir.on_create(target.code)


@event.listens_for(Item.code, 'set')
def receive_set(target, value, oldvalue, initiator):
    """Catches item modification and reroutes event."""
    fs_mngr.storage.dir.on_modify(oldvalue, value)


@event.listens_for(Item, 'after_delete')
def receive_after_delete(mapper, connection, target):
    """Catches item delete and reroutes event."""
    fs_mngr.storage.dir.on_delete(target.code)
