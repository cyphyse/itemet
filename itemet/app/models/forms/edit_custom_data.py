# -*- coding: <utf-8>
# internal
from ... import db
from .. data.item import Item
# external
from flask_babel import lazy_gettext as _
from flask_appbuilder.forms import DynamicForm
from flask_appbuilder.fieldwidgets import (
    BS3TextFieldWidget,
    Select2Widget,
    BS3TextAreaFieldWidget
)
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField


class ItemSelectModel(DynamicForm):

    item = QuerySelectField(
        _('Select Item'),
        query_factory=lambda: db.session.query(Item),
        widget=Select2Widget()
    )


class ItemCustomEditModel(DynamicForm):

    code = StringField(
        _("Item"),
        description=("Item to edit"),
        validators=[DataRequired()],
        widget=BS3TextFieldWidget(),
        render_kw={'readonly': True}
    )
    default = StringField(
        _("Type YAML format"),
        description=("Defined YAML format for items of that type"),
        widget=BS3TextAreaFieldWidget(),
        render_kw={'readonly': True}
    )
    custom = StringField(
        _("Item custom data"),
        description=("Actual custom data of this item"),
        widget=BS3TextAreaFieldWidget()
    )
