# -*- coding: <utf-8>
# internal
from .... import db

from .... models.forms.file_upload import FileUpload
from .... models.data.item import Item

from .... import app
import os
from flask import flash
from .... extension.form_extensions import SimplePkFormView
from flask_babel import lazy_gettext as _

from werkzeug.utils import secure_filename

from .... interface.filesystem import orm


class FileUploadForm(SimplePkFormView):
    form = FileUpload
    form_title = 'This is my first form view'
    message = 'My form submitted'

    def form_get(self, form):
        i = db.session.query(Item).filter_by(id=int(form.pk)).first()
        form.code.data = i.code

    def form_post(self, form):
        f = form.file.data
        filename = secure_filename(f.filename)
        fn = os.path.join(orm.fs.get_asset_path(form.code.data), filename)
        f.save(fn)
        # post process form
        flash("Saved data to" + fn, 'info')
