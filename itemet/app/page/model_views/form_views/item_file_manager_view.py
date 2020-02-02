# -*- coding: <utf-8>
# internal
from .... import db
from .... extension.form_extensions import SimplePkFormView
from .... interface.filesystem import orm
from .... models.forms.item_file_manager import ItemFileManager
from .... models.data.item import Item
# external
import os
import glob
from flask import flash
from werkzeug.utils import secure_filename


class ItemFileManagerView(SimplePkFormView):
    form = ItemFileManager
    form_title = 'Item File Manager'
    message = 'My form submitted'

    def form_get(self, form):
        i = db.session.query(Item).filter_by(id=int(form.pk)).first()
        form.code.data = i.code

        item_path = os.path.join(orm.fs.get_asset_path(form.code.data), '*')
        item_files = glob.glob(item_path)

        form.file_links.choices = []
        for item_file in item_files:
            filename = os.path.basename(item_file)
            # TODO get correct path
            a = "<a href=\"/files/db/itemet.db/asset/" + form.code.data + "/" + filename + "\"" \
                + " title=\"" + item_file + "\">" + filename + "</a>"
            form.file_links.choices.append((filename, a))

        form.files_to_delete.choices = [("-", "-")]
        for item_file in item_files:
            filename = os.path.basename(item_file)
            form.files_to_delete.choices.append((filename, filename))
        form.files_to_delete.pre_validate = lambda f: None

    def form_post(self, form):

        def delete(item_code, filename):
            nonlocal txt
            if len(filename) > 0 and not filename == "-":
                filepath = orm.fs.get_asset_path(form.code.data, filename)
                os.remove(filepath)
                txt += " | Deleted: " + filepath

        def save(item_code, file):
            nonlocal txt
            filename = secure_filename(file.filename)
            if len(filename) > 0:
                filepath = orm.fs.get_asset_path(item_code, filename)
                file.save(filepath)
                txt += " | Saved: " + filename

        txt = ""
        files_to_delete = form.files_to_delete.data
        if files_to_delete is None:
            txt += " nothing"
        elif isinstance(files_to_delete, list):
            for filename in files_to_delete:
                delete(form.code.data, filename)
        else:
            delete(form.code.data, files_to_delete)

        files_to_upload = form.files_to_upload.data
        if files_to_upload is None:
            pass
        elif isinstance(files_to_upload, list):
            for file in files_to_upload:
                save(form.code.data, file)
        else:
            save(form.code.data, files_to_upload)

        flash("Operations: " + txt[3:], 'info')
