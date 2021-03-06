# -*- coding: <utf-8>
# internal
from .... import db
from csvdoc.document_transform import DocumentTransform
# external
import os
import json

transform = DocumentTransform()


class StorageItemDocument(object):
    """
    This class provides functions to create
    documents in markdown and json format from a db entry.
    """

    def __init__(self, fs):
        self.name = "Document"
        self.fs = fs

    def make(self, item):
        item_code = item.code
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

        def get_cleaned_path(item_code, ext):
            filepath = self.fs.get_asset_path(item_code, item_code + ext)
            try:
                os.remove(filepath)
            except Exception as err:
                pass
            return filepath

        filepath = get_cleaned_path(item_code, ".json")
        with open(filepath, 'w', encoding='utf-8') as fp:
            json.dump(final_dict, fp, indent=2, ensure_ascii=False)
        json_filepath = filepath
        filepath = get_cleaned_path(item_code, ".md")
        final_doc = transform.to_doc(final_dict)
        with open(filepath, 'w', encoding='utf-8') as fp:
            fp.write(final_doc)
        md_filepath = filepath
        return [json_filepath, md_filepath]
