# -*- coding: <utf-8>
# internal
from .. import app, db
from .. models.data.item import Item
from csvdoc.document_transform import DocumentTransform
# external
import os
import json

transform = DocumentTransform()


class Document(object):
    """
    This class provides functions to create
    documents in markdown and json format from a db entry.
    """

    def __init__(self):
        self.name = "Document"

    def make(self, item_code):
        item = db.session.query(Item).filter_by(code=item_code).first()
        # get all data
        item_base = item.as_doc_dict()
        # extract custom yamlmd
        item_custom_yamlmd = item_base.pop("custom")
        # get fields from yamlmd
        item_custom = transform.to_dict(item_custom_yamlmd)
        # seperate markdown text
        item_custom_md = item_custom.pop("markdown", "")
        # create dict with all data
        final_dict = {
            "base": item_base,
            "custom": item_custom,
            "markdown": item_custom_md
        }
        filedir = app.config['ITEMET'].get("path").get("selected").get("input")
        filepath = os.path.join(filedir, item_code + ".json")
        with open(filepath, 'w', encoding='utf-8') as fp:
            json.dump(final_dict, fp, indent=2, ensure_ascii=False)
        json_filepath = filepath
        filepath = os.path.join(filedir, item_code + ".md")
        final_doc = transform.to_doc(final_dict)
        with open(filepath, 'w', encoding='utf-8') as fp:
            fp.write(final_doc)
        md_filepath = filepath
        return [json_filepath, md_filepath]
