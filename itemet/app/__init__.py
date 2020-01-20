# internal
# external
import os
from flask import Flask
from flask_appbuilder import IndexView, AppBuilder, SQLA
# logging
import logging
logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger(__file__)

# Create application
app = Flask(__name__)

# Load configuration
app.config.from_object("config")
if 'ITEMET_CONFIG' in os.environ:
    logger.info("Load config from: " + os.environ.get('ITEMET_CONFIG'))
    app.config.from_envvar('ITEMET_CONFIG')

# Create directories
paths = [
    app.config['ITEMET']['path']['selected']['input'],
    app.config['ITEMET']['path']['csvdoc']['export']['items'],
    app.config['ITEMET']['path']['csvdoc']['export']['net_config'],
]
dbs = app.config['SQLALCHEMY_DATABASE_URI']
if "sqlite" in dbs:
    paths.append(dbs.replace("sqlite:///", ""))
for p in paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)


# Initialize dependencies
class MainIndexView(IndexView):
    index_template = 'itemet_index.html'


db = SQLA(app)
appbuilder = AppBuilder(
    app, db.session,
    base_template='itemet_base.html', indexview=MainIndexView
)

# Load plugins
from app.interface.trigger import plugintrigger
cfg = app.config
icfg = app.config['ITEMET']
plugintrigger.init(
    icfg["path"]["plugin"]["pattern"],
    icfg["path"]["plugin"]["out"]
)

# Load page
from . import page
