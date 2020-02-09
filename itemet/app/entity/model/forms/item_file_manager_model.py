# -*- coding: <utf-8>
# internal
from .. format import fmt
# external
from markupsafe import Markup
from flask_babel import lazy_gettext as _
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from wtforms import StringField, SelectMultipleField, MultipleFileField
from wtforms.validators import DataRequired
from wtforms.widgets.core import html_params


class NonValidatingSelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        pass


class LinkListWidget(object):

    def __init__(self, html_tag="ul"):
        assert html_tag in ("ol", "ul")
        self.html_tag = html_tag

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = ["<%s %s>" % (self.html_tag, html_params(**kwargs))]
        for subfield in field:
            html.append("<li>%s</li>" % subfield.label)
        html.append("</%s>" % self.html_tag)
        return Markup("".join(html))


class LinkListField(NonValidatingSelectMultipleField):
    widget = LinkListWidget()


class ItemFileManager(DynamicForm):
    code = StringField(
        _("Item"),
        description=_("Item to edit"),
        validators=[DataRequired()],
        widget=BS3TextFieldWidget(),
        render_kw={'readonly': True}
    )

    file_links = LinkListField(
        _("Files to download"),
        description=_("Select a file to download"),
    )

    files_to_delete = NonValidatingSelectMultipleField(
        _("Files to delete"),
        description=_("Select one or more files to delete"),
    )
    files_to_upload = MultipleFileField(
        _("Files to upload"),
        description=_("Select one or more files to upload"),
    )
