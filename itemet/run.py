import os
from app import app
from flask_autoindex import AutoIndex


app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

serve_path = os.path.abspath(
    app.config['ITEMET'].get("path").get("flask").get("serve")
)

files_index = AutoIndex(app, browse_root=serve_path, add_url_rules=False)

@app.route('/files')
@app.route('/files/<path:path>')
def autoindex(path='.'):
    return files_index.render_autoindex(path)

app.run(host="0.0.0.0", port=8080, debug=True)
