# -*- coding: <utf-8>
# internal
from .... import app, db
from .... entity.model.objects.item_state_model import ItemState
from .... entity.model.objects.item_type_model import ItemType
from .... entity.operation.functions import _2db
# external
import os
import json
import yaml
# logging
import logging
logger = logging.getLogger(__name__)


class NetworkConfiguration(object):
    """
    Class to handle the network configuration in file system representation.
    """

    def add_net_config_to_db(self):
        # load dict
        filepath = app.config['ITEMET'].get("path").get("itemet net_config")
        with open(filepath) as net_cfg_file:
            net_cfg = json.load(net_cfg_file)
        # process data
        for type_code, type_item in net_cfg.items():
            state_codes = type_item.get("state", {})
            need_codes = type_item.get("need", {})
            custom = type_item.get("custom", None)
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
            if custom is None:
                c_obj = ""
            else:
                c_obj = yaml.dump(custom, default_flow_style=False, allow_unicode=True)
            # create type
            param = {
                "type": type_code,
                "type_states": states,
                "type_needs": needs,
                "custom_template": c_obj
            }
            _2db(ItemType, param, {"type_code": type_code})

    def export_net_config_to_fs(self):
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
