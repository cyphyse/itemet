# -*- coding: <utf-8>
# internal
from .. import app, db
from .. models.data.item_state import ItemState
from .. models.data.item_type import ItemType
from .. models.data.item import Item
from . trigger import plugintrigger
from . document import Document
from csvdoc.table_collection import TableCollection
# external
import os
import glob
import json
import yaml
import pandas as pd
# logging
import logging
logger = logging.getLogger(__name__)

KEY_BASE = "base"
KEY_CUSTOM = "custom"


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


class PandasPort(object):

    def clear_db(self):
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

    def add_net_config_to_db(self):
        # load dict
        filepath = app.config['ITEMET'].get("path").get("itemet net_config")
        with open(filepath) as net_cfg_file:
            net_cfg = json.load(net_cfg_file)
        # process data
        for type_code, type_item in net_cfg.items():
            state_codes = type_item.get("state", {})
            need_codes = type_item.get("need", {})
            custom = type_item.get("custom", "---\n---")
            # find or add states
            states = []
            for state_code, state_color in state_codes.items():
                s_param = {"state": state_code, "color": state_color}
                s_obj = _2db(ItemState, s_param, {"state_code": state_code})
                states.append(s_obj)
            # find or add needs
            needs = []
            for need_code, need_active in need_codes.items():
                n_param = {"type": need_code}
                n_obj = _2db(ItemType, n_param, {"type_code": need_code})
                needs.append(n_obj)
            # dict to yaml
            c_obj = yaml.dump(custom, default_flow_style=False, allow_unicode=True)
            # create type
            param = {
                "type": type_code,
                "type_states": states,
                "type_needs": needs,
                "custom_template": c_obj
            }
            _2db(ItemType, param, {"type_code": type_code})


    def create_net_config_from_db(self):
        # net config
        net_config = {}
        types = db.session.query(ItemType).all()
        for type in types:
            net_config.update({type.type_code: {}})
            # add states
            states = {}
            for s in type.type_states:
                states.update({s.state_code: s.state_color})
            net_config[type.type_code].update({"state": states})
            # add needs
            needs = {}
            for n in type.type_needs:
                needs.update({n.type_code: "true"})
            net_config[type.type_code].update({"need": needs})
            # add custom data
            if type.custom_template is not None:
                for doc in yaml.load_all(type.custom_template):
                    if isinstance(doc, dict):
                        net_config[type.type_code].update({"custom": doc})
        filepath = app.config['ITEMET'].get("path").get("itemet net_config")

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w") as net_cfg_file:
            json.dump(net_config, net_cfg_file, indent=4)

    def add_df_to_db(self, df):
        for idx_row, row in df.iterrows():
            d = df.loc[idx_row].to_dict()
            d["state"] = get_T(ItemState, {"state_code": d["state"]})
            d["type"] = get_T(ItemType, {"type_code": d["type"]})
            li = []
            for n in d["need"]:
                if n is not None and not n == "" and not n == "''":
                    li.append(_2db(Item, {"code": n}, {"code": n}))
            d["need"] = li
            _2db(Item, d, {"code": d["code"]})

    def import_table(self):
        self.clear_db()
        self.add_net_config_to_db()
        filepattern = app.config['ITEMET'].get("path").get("itemet items")
        files = glob.glob(filepattern + "/*.csv")
        self.csv_db = TableCollection(files=files)
        self.csv_db.load()
        for df in self.csv_db.get_document_shaped([KEY_CUSTOM]):
            df.columns = [col.replace(KEY_BASE + ".", "") for col in df]
            self.add_df_to_db(df)
        db.session.commit()

    def export_table(self):
        items = db.session.query(Item).all()
        base_path = app.config['ITEMET'].get("path").get("itemet items")
        os.makedirs(base_path, exist_ok=True)
        # collect items for each type TODO: improve this by useing db functions
        data_model = {}  # create one file for each type
        for item in items:
            type = str(item.type)
            filepath = os.path.join(base_path, type + ".csv")
            if filepath not in data_model:
                data_model.update({filepath: []})
            data_model[filepath].append(item.as_dict())
        # create data model for csvdoc database
        db_model = {}
        for path, data in data_model.items():
            tmp = pd.DataFrame.from_records(data)
            cols = []
            for col in tmp:
                if col == KEY_CUSTOM:
                    cols.append(col)
                else:
                    cols.append(KEY_BASE + "." + col)
            tmp.columns = cols
            db_model.update({path: tmp})

        self.csv_db = TableCollection(files=list(db_model.keys()))
        self.csv_db.set_document_shaped(list(db_model.values()), [KEY_CUSTOM])
        self.csv_db.save()
        self.create_net_config_from_db()
        plugintrigger.on_event(base_path)

    def set_selected(self, item_code):
        doc = Document()
        files = doc.make(item_code)
        plugintrigger.on_event(files[0])
        plugintrigger.on_event(files[1])
