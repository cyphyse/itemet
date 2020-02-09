# -*- coding: <utf-8>
# internal
from .... import app, db
from .... entity.model.objects.item_state_model import ItemState
from .... entity.model.objects.item_type_model import ItemType
from .... entity.model.objects.item_model import Item
from . helper import get_T, _2db
# library
from csvdoc.table_collection import TableCollection
# external
import os
import glob
import pandas as pd
# logging
import logging
logger = logging.getLogger(__name__)

KEY_BASE = "base"
KEY_CUSTOM = "custom"


class NetworkTables(object):

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

    def add_net_tables_to_db(self):
        filepattern = app.config['ITEMET'].get("path").get("itemet items")
        files = glob.glob(filepattern + "/*.csv")
        self.csv_db = TableCollection(files=files)
        self.csv_db.load()
        for df in self.csv_db.get_document_shaped([KEY_CUSTOM]):
            df.columns = [col.replace(KEY_BASE + ".", "") for col in df]
            self.add_df_to_db(df)
        db.session.commit()

    def export_net_tables_to_fs(self):
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
