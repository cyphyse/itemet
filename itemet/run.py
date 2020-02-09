# -*- coding: <utf-8>
# internal
from app import app
from app.interface.filesystem.manager import fs_mngr
# external
import os
from flask_autoindex import AutoIndex

# assign path from configuration to orm file system extension
p = app.config['ITEMET'].get("path").get("itemet items")
asset = os.path.join(p, "asset")
trash = os.path.join(p, "trash")
fs_mngr.storage.dir.init_paths(asset=asset, trash=trash)

# configure flask to tell the client to not take cached downlaods
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# create file server and store path to config to be able to link to files
serve_path = app.config['ITEMET'].get("path").get("itemet db")
files_index = AutoIndex(app, browse_root=serve_path, add_url_rules=False)

# add file server
@app.route('/files')
@app.route('/files/<path:path>')
def autoindex(path='.'):
    return files_index.render_autoindex(path)


app.run(host="0.0.0.0", port=8080, debug=True)
