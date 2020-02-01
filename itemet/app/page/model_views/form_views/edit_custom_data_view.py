# -*- coding: <utf-8>
# internal
from .... import db
from .... models.forms.edit_custom_data import ItemCustomEditModel
from .... models.data.item import Item
from .... extension.form_extensions import SimplePkFormView
from .... interface.port import PandasPort
from csvdoc.document_transform import DocumentTransform
# external
from flask import redirect, flash
from flask_babel import lazy_gettext as _
# logging
import logging
logger = logging.getLogger(__name__)


transform = DocumentTransform()


class ItemCustomEditView(SimplePkFormView):
    """
    View to provide the edit of custom data via an action button in model view.
    """
    form = ItemCustomEditModel
    form_title = _("")
    message_info = _("Saved!")
    message_warn = _("Invalid!")

    def form_get(self, form):
        i = db.session.query(Item).filter_by(id=int(form.pk)).first()
        if i is None:
            logger.error("No item was found!")
            return redirect("/itemcustomeditview/form")
        form.code.data = i.code
        if i.type is not None:
            form.default.data = i.type.custom_template

        if i.custom is None or i.custom == "":
            form.custom.data = i.type.custom_template
        else:
            form.custom.data = i.custom

    def form_post(self, form):
        port = PandasPort()
        i = db.session.query(Item).filter_by(code=form.code.data).first()
        template = i.type.custom_template
        if transform.valid_fields(template, form.custom.data):
            i.custom = form.custom.data.strip()
            # add data separator if its missing
            if "\n---" not in template:
                template += "\n---"
            tmp = transform.to_dict(template)
            data_in_template = len(tmp.keys()) > 1
            tmp = i.custom.splitlines()
            separator_is_missing = "---" not in tmp[1:]
            if data_in_template and separator_is_missing:
                i.custom += "\n---"
            # save changes and proceed
            db.session.commit()
            port.set_selected(i.code)
            flash(self.message_info, "info")
        else:
            flash(self.message_warn, "warning")
