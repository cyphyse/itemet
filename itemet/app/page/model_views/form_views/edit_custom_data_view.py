# -*- coding: <utf-8>
# internal
from .... import db
from .... models.forms.edit_custom_data import ItemCustomEditModel
from .... models.data.item import Item
from .... extension.form_extensions import SimplePkFormView
from .... interface.port import PandasPort
from csvdoc.document_compare import DocumentCompare
# external
from flask import redirect, flash
from flask_babel import lazy_gettext as _
# logging
import logging
logger = logging.getLogger(__name__)


compare = DocumentCompare()


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
        template = template.strip()
        # ensure that compare take template data as yaml data
        if not template.split("\n")[-1] == "---":
            template += "\n---"
        cr = compare.fields(template, form.custom.data)
        if cr:
            # take separator cleand data from validation because
            # it will determine the correct data based on template
            # even if a separator is missing
            i.custom = cr.cmp
            # save changes and proceed
            db.session.commit()
            port.set_selected(i.code)
            flash(self.message_info, "info")
        else:
            flash(self.message_warn, "warning")
