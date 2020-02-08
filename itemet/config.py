# -*- coding: <utf-8>
# internal
import os
import json
# external
from flask.cli import with_appcontext
from flask_appbuilder.security.manager import (
    AUTH_OID,
    AUTH_REMOTE_USER,
    AUTH_DB,
    AUTH_LDAP,
    AUTH_OAUTH,
)
# logging
import logging
logger = logging.getLogger(__file__)

basedir = os.path.abspath(os.path.dirname(__file__))


# ---------------------------------------------------
# Helper functions for Itemet
# ---------------------------------------------------

def load_from_json(path):
    """
    Loads a base configuration from a json file.
    """
    with open(path) as cfg_file:
        ITEMET = json.load(cfg_file)
    return ITEMET


def make_paths_absolute(path_dict, root_dir):
    """
    Returns a dict with absolute paths contructed to a given root dir.
    """
    for key, path in path_dict.items():
        if isinstance(path, dict):
            path_dict[key] = make_paths_absolute(path)
        else:
            path_dict[key] = os.path.abspath(os.path.join(root_dir, path))
    return path_dict


# Determine path to Itemet configuration
if 'ITEMET_CONFIG' in os.environ:
    # take path from environment variable
    itemet_conf_path = os.environ.get('ITEMET_CONFIG')
else:
    # take default configuration path
    itemet_conf_path = os.path.join(basedir, "config.json")

# Load base configuration for itemet from json-file and preprocess paths
logger.info("Load config from: " + itemet_conf_path)
ITEMET = load_from_json(itemet_conf_path)
ITEMET["path"] = make_paths_absolute(
    ITEMET["path"],
    os.path.dirname(itemet_conf_path)
)

# ---------------------------------------------------
# Apply itemet config to flask settings
# ---------------------------------------------------
# The SQLAlchemy connection string
if ITEMET["flask db"] == "sqlite":
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + ITEMET["path"]["flask db"]
else:
    SQLALCHEMY_DATABASE_URI = ITEMET["flask db"]

# Your App secret key
SECRET_KEY = ITEMET["secret key"]

# ------------------------------
# GLOBALS FOR APP Builder
# ------------------------------
# Flask-WTF flag for CSRF
CSRF_ENABLED = True

# Uncomment to setup Your App name
APP_NAME = "Itemet"

# Uncomment to setup Setup an App icon
# APP_ICON = "static/img/logo.jpg"

# ----------------------------------------------------
# AUTHENTICATION CONFIG
# ----------------------------------------------------
# The authentication type
# AUTH_OID : Is for OpenID
# AUTH_DB : Is for database (username/password()
# AUTH_LDAP : Is for LDAP
# AUTH_REMOTE_USER : Is for using REMOTE_USER from web server
AUTH_TYPE = AUTH_DB

# Uncomment to setup Full admin role name
# AUTH_ROLE_ADMIN = 'Admin'

# Uncomment to setup Public role name, no authentication needed
# AUTH_ROLE_PUBLIC = 'Public'

# Will allow user self registration
# AUTH_USER_REGISTRATION = True

# The default user self registration role
# AUTH_USER_REGISTRATION_ROLE = "Public"

# When using LDAP Auth, setup the ldap server
# AUTH_LDAP_SERVER = "ldap://ldapserver.new"

# Uncomment to setup OpenID providers example for OpenID authentication
# OPENID_PROVIDERS = [
#    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
#    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
#    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
#    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
# ---------------------------------------------------
# Babel config for translations
# ---------------------------------------------------
# Setup default language
BABEL_DEFAULT_LOCALE = "en"
# Your application default translation path
BABEL_DEFAULT_FOLDER = "translations"
# The allowed translation for you app
LANGUAGES = {
    "en": {"flag": "gb", "name": "English"},
    #    "pt": {"flag": "pt", "name": "Portuguese"},
    #    "pt_BR": {"flag": "br", "name": "Pt Brazil"},
    #    "es": {"flag": "es", "name": "Spanish"},
    #    "de": {"flag": "de", "name": "German"},
    #    "zh": {"flag": "cn", "name": "Chinese"},
    #    "ru": {"flag": "ru", "name": "Russian"},
    #    "pl": {"flag": "pl", "name": "Polish"},
}
# ---------------------------------------------------
# Image and file configuration
# ---------------------------------------------------
# The file upload folder, when using models with files
UPLOAD_FOLDER = basedir + "/app/static/uploads/"

# The image upload folder, when using models with images
IMG_UPLOAD_FOLDER = basedir + "/app/static/uploads/"

# The image upload url, when using models with images
IMG_UPLOAD_URL = "/static/uploads/"
# Setup image size default is (300, 200, True)
# IMG_SIZE = (300, 200, True)

# Theme configuration
# these are located on static/appbuilder/css/themes
# you can create your own and easily use them placing them on the same dir structure to override
# APP_THEME = "bootstrap-theme.css"  # default bootstrap
# APP_THEME = "cerulean.css"
# APP_THEME = "amelia.css"
# APP_THEME = "cosmo.css"
# APP_THEME = "cyborg.css"
# APP_THEME = "flatly.css"
# APP_THEME = "journal.css"
# APP_THEME = "readable.css"
# APP_THEME = "simplex.css"
# APP_THEME = "slate.css"
# APP_THEME = "spacelab.css"
# APP_THEME = "united.css"
# APP_THEME = "yeti.css"
