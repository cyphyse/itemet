import os
from app import app
from app.interface.filesystem import orm
from flask_autoindex import AutoIndex


p = app.config['ITEMET'].get("path").get("csvdoc").get("export").get("items")
asset = os.path.join(p, "asset")
trash = os.path.join(p, "trash")
orm.init_paths(asset=asset, trash=trash)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

serve_path = os.path.abspath(
    app.config['ITEMET'].get("path").get("flask").get("serve")
)
app.config['ITEMET']['path']['flask']['fullserve'] = serve_path

files_index = AutoIndex(app, browse_root=serve_path, add_url_rules=False)

@app.route('/files')
@app.route('/files/<path:path>')
def autoindex(path='.'):
    return files_index.render_autoindex(path)


app.run(host="0.0.0.0", port=8080, debug=True)
