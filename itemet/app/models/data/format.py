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
    """
    Commonly used class to format data.
    """

    def __init__(self):
        pass

    def list2html(self, list, link_url=True):
        """
        Returns a list as html code.
        """
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
        """
        Returns a markdown document in html.
        """
        return Markup(markdown.markdown(doc))

    def code(self, code):
        """
        Returns a code which can be used as a filename.
        """
        return sanitize_filename(code)

    def number(self, num):
        """
        Returns a given number of any type as float if possible else 0.0.
        """
        if not isinstance(num, float):
            try:
                num = float(num)
            except Exception as err:
                err_txt = "'" + str(num) + "'"
                err_txt += " is not a number (" + str(err) + ")!"
                logger.error(err_txt)
                num = 0.0
        return num


"""Main access to formatting."""
fmt = Format()
