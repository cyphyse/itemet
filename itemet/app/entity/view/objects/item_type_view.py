# -*- coding: <utf-8>
# internal
from ... model.objects.item_type_model import ItemType
# external
from flask_babel import lazy_gettext as _
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView


class ItemTypeView(ModelView):
    datamodel = SQLAInterface(ItemType)
    add_columns = ['type_code', 'type_states', 'type_needs', 'custom_template']
    edit_columns = add_columns
    view_colums = ['type_code', 'type_states_view', 'type_needs_view', 'custom_template_view']
    list_columns = view_colums
    show_columns = view_colums
    label_columns = {
        'type_code': _('Code'),
        'custom_template':_('YAML Format'), 'custom_template_view': _('YAML Format'),
        'type_needs': _('Needs'), 'type_needs_view': _('Needs'),
        'type_states': _('States'), 'type_states_view': _('States')
    }
