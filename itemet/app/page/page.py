# -*- coding: <utf-8>
# internal
from .. import appbuilder, db
from .. interface.endpoints import ApiEndpoints
from . tabs import add_data_tab, add_edit_tab
# external
from flask import render_template
from flask_babel import lazy_gettext as _

# init database
db.create_all()
# add endpoints
appbuilder.add_view_no_menu(ApiEndpoints)
# add tabs
add_data_tab()
add_edit_tab()

"""
    Application wide 404 error handler
"""
@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html",
            base_template=appbuilder.base_template,
            appbuilder=appbuilder
        ),
        404,
    )
