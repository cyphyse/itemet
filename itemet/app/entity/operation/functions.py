# -*- coding: <utf-8>
# internal
from ... import db
from .. model.objects.item_state_model import ItemState
from .. model.objects.item_type_model import ItemType
from .. model.objects.item_model import Item
# external
# logging
import logging
logger = logging.getLogger(__name__)


def get_T(T, search):
    return db.session.query(T).filter_by(**search).first()


def itelligent_search_add(T, param, search):
    """Search in db with 'search' creteria and
    creates object from 'param' if nothing was found"""
    # TODO: consider to use refresh function
    # TODO: consider to use merge function
    Q = db.session.query(T).filter_by(**search).all()
    assert len(Q) < 2, "There is a bad bug in here!"
    if len(Q) == 0:  # create if not exisits
        Q = [T().from_dict(param)]
        db.session.add(Q[0])
    else:  # update the existing
        Q[0] = Q[0].from_dict(param)
    if not Q[0].is_valid():
        logger.warning("Deleted entry with data: " + str(param))
        db.session.delete(Q[0])
        return None
    return Q[0]


_2db = itelligent_search_add  # it's just shorter


def clear_db():
    # delete all connections first
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
