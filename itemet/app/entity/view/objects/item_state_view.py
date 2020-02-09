# -*- coding: <utf-8>
# internal
from ... model.objects.item_state_model import ItemState
# external
from flask_babel import lazy_gettext as _
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView


class ItemStateView(ModelView):
    datamodel = SQLAInterface(ItemState)
    all_columns = ['state_code', 'state_color']
    list_columns = all_columns
    show_columns = all_columns
    edit_columns = all_columns
    label_columns = {
        'state_code': _('Code'),
        'state_color': _('Color'),
    }
