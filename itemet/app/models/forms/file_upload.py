from wtforms import Form, StringField
from wtforms.validators import DataRequired
from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
from flask_appbuilder.forms import DynamicForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_babel import lazy_gettext as _



class FileUpload(DynamicForm):
    code = StringField(
        _("Item"),
        description=("Item to edit"),
        validators=[DataRequired()],
        widget=BS3TextFieldWidget(),
        render_kw={'readonly': True}
    )
    file = FileField(
        _("File"),
        validators=[FileRequired()]
    )
