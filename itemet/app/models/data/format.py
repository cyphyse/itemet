# -*- coding: <utf-8>
# external
import markdown
from pathvalidate import sanitize_filename
from flask import url_for
from flask import Markup
# logging
import logging
logger = logging.getLogger()


class Format(object):
    def __init__(self):
        pass

    def list2html(self, list, link_url=True):
        html = "<dl>"
        for entry in list:
            if link_url:
                link = '<a href="' + url_for('ItemMasterView.show', pk=str(entry.id)) + '">' + str(entry) + '</a>'
            else:
                link = str(entry)
            html += "<dd>" + link + "</dd>"
        html += "</dl>"
        return Markup(html)

    def doc2html(self, doc):
        return Markup(markdown.markdown(doc))

    def code(self, code):
        return sanitize_filename(code)

    def number(self, num):
        if not isinstance(num, float):
            try:
                num = float(num)
            except:
                logger.error("'" + str(num) + "' is not a number!")
                num = 0.0
        return num

fmt = Format()
