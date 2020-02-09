# -*- coding: <utf-8>
# internal
from .... import db
from .... extension.form_extensions import (
    AJAXSelectManyField,
    SelectMany2SlaveAJAXWidget
)
from ... model.objects.item_model import Item
# external
from pathvalidate import validate_filename
from flask import redirect
from flask_babel import lazy_gettext as _
from flask_appbuilder import ModelView
from flask_appbuilder.actions import action
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.fields import AJAXSelectField
from flask_appbuilder.fieldwidgets import (
    Select2AJAXWidget,
    Select2SlaveAJAXWidget
)
from sqlalchemy.orm.session import make_transient




def validate_this_filename(form, field):
    validate_filename(str(field.data))


ITEM_BASE_COLS = ['code', 'type', 'start', 'end']
ITEM_DBNW_COLS = ITEM_BASE_COLS + ['needs', 'state', 'status']
ITEM_FULL_COLS = ITEM_DBNW_COLS + ['needs', 'state', 'status', 'custom']
COLS_LIST = ITEM_BASE_COLS + ['needs_view', 'state', 'status']
COLS_ADD = ITEM_FULL_COLS
COLS_EDIT = ITEM_FULL_COLS
COLS_SHOW = COLS_LIST + ['custom_view']


def get_extra_fields(datamodel):
    extra_fields = {}
    extra_fields.update({"type": AJAXSelectField(_("Item Type"),
            description=_("Defines needs, states and yaml format"),
            datamodel=datamodel, col_name="type",
            widget=Select2AJAXWidget(
                endpoint="/itemmasterview/api/column/add/type"
            )
        )
    })
    extra_fields.update({"needs": AJAXSelectManyField(_("Item Needs"),
            description=_("Needs related to type"),
            datamodel=datamodel, col_name="needs",
            widget=SelectMany2SlaveAJAXWidget(
                endpoint_opt="/apiendpoints/itemsfortype/{{ID}}",
                endpoint_sel="/apiendpoints/needsofitem/{{ID}}",
                master_id="type",
            )
        )
    })
    extra_fields.update({"state": AJAXSelectField(_("Item State"),
            description=_("State related to type"),
            datamodel=datamodel, col_name="state",
            widget=Select2SlaveAJAXWidget(
                endpoint="/apiendpoints/statesfortype/{{ID}}",
                master_id="type"
            )
        )
    })
    return extra_fields


def get_fieldsets():
    fieldsets = [
        ('Network Data', {'fields': ITEM_DBNW_COLS}),
        ('Custom Data',  {'fields': ['custom'], 'expanded': False})
    ]
    return fieldsets


def get_label():
    LABEL_CUSTOM = "Custom Data"
    LABEL_NEEDS = "Needs"
    res = {
        'custom_view': LABEL_CUSTOM, 'custom': LABEL_CUSTOM,
        'needs_view': LABEL_NEEDS, 'needs': LABEL_NEEDS
    }
    return res


class ItemView(ModelView):
    datamodel = SQLAInterface(Item)
    list_columns = COLS_LIST
    add_columns = COLS_ADD
    edit_columns = COLS_EDIT
    show_columns = COLS_SHOW
    search_columns = ITEM_FULL_COLS
    validators_columns = {'code': [validate_this_filename]}
    add_form_extra_fields = edit_form_extra_fields = \
        get_extra_fields(datamodel)
    add_fieldsets = edit_fieldsets = \
        get_fieldsets()
    label_columns = \
        get_label()


class ItemMasterView(ModelView):
    datamodel = SQLAInterface(Item)
    related_views = [ItemView]
    show_template = 'appbuilder/general/model/show_cascade.html'
    edit_template = 'appbuilder/general/model/edit_cascade.html'

    list_columns = COLS_LIST
    add_columns = COLS_ADD
    edit_columns = COLS_EDIT
    show_columns = COLS_SHOW
    search_columns = ITEM_FULL_COLS
    validators_columns = {'code': [validate_this_filename]}
    add_form_extra_fields = edit_form_extra_fields = \
        get_extra_fields(datamodel)
    add_fieldsets = edit_fieldsets = \
        get_fieldsets()
    label_columns = \
        get_label()


    @action("duplicate", "Duplicate", confirmation="Duplicate entry?", icon="fa-copy", single=True, multiple=False)
    def duplicate(self, item):
        code = item.code
        db.session.expunge(item)
        make_transient(item)
        # http://docs.sqlalchemy.org/en/rel_1_1/orm/session_api.html#sqlalchemy.orm.session.make_transient
        item.id = None
        item.code = code + "__COPY__"
        db.session.add(item)
        db.session.commit()
        db.session.refresh(item)
        return redirect("/itemmasterview/edit/" + str(item.id))

    @action("customeditaction", _("Edit custom data"), confirmation="Change entry?", icon="fa-pencil", single=True, multiple=False)
    def customeditaction(self, item):
        return redirect("/apiendpoints/editcustomdata/" + str(item.id))

    @action("filemanager", _("Manage Files"), confirmation="Open file manager?", icon="fa-file", single=True, multiple=False)
    def filemanager(self, item):
        return redirect("/apiendpoints/filemanager/" + str(item.id))
