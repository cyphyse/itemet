# -*- coding: <utf-8>
# internal
from .. import appbuilder
from .. entity.view.objects.item_state_view import ItemStateView
from .. entity.view.objects.item_type_view import ItemTypeView
from .. entity.view.objects.item_view import ItemView, ItemMasterView
from .. entity.view.forms.edit_custom_data_view import ItemCustomEditView
from .. entity.view.forms.item_file_manager_view import ItemFileManagerView

# external
from flask_babel import lazy_gettext as _


def add_data_tab():
    """Adds data tab"""
    CATEGORY = 'Data'
    ICON = 'fa-folder-open-o'
    appbuilder.add_link(
        'Import Data',
        href='/apiendpoints/importdata/None',
        icon='fa-download',
        label=_('Import'),
        category=CATEGORY,
        category_icon=ICON,
        category_label=_(CATEGORY)
    )
    appbuilder.add_link(
        'Export Data',
        href='/apiendpoints/exportdata/None',
        icon='fa-upload',
        label=_('Export'),
        category=CATEGORY,
        category_icon=ICON,
        category_label=_(CATEGORY)
    )
    appbuilder.add_link(
        'Browse Data',
        href='/files',
        icon='fa-folder-open',
        label=_('Browse'),
        category=CATEGORY,
        category_icon=ICON,
        category_label=_(CATEGORY)
    )


def add_edit_tab():
    """Adds edit tab"""
    CATEGORY = 'Edit'
    ICON = 'fa-pencil'
    appbuilder.add_view(
        ItemStateView,
        'Configure States',
        icon='fa-delicious',
        label=_('States'),
        category=CATEGORY,
        category_icon=ICON,
        category_label=_(CATEGORY)
    )
    appbuilder.add_view(
        ItemTypeView,
        'Configure Types',
        icon='fa-cubes',
        label=_('Types'),
        category=CATEGORY,
        category_icon=ICON,
        category_label=_(CATEGORY)
    )
    appbuilder.add_view_no_menu(ItemCustomEditView)
    appbuilder.add_view_no_menu(ItemFileManagerView)
    appbuilder.add_view_no_menu(ItemView)
    appbuilder.add_view(
        ItemMasterView,
        'Edit Items',
        icon='fa-table',
        label=_('Items'),
        category=CATEGORY,
        category_icon=ICON,
        category_label=_(CATEGORY)
    )
