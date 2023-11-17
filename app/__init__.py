from flask import Flask

import configs

app = Flask(__name__)
app.config.from_object(configs.Config)
# Route to serve the static files, i.e css
@app.route('/static/<path:filename>')
def serve_static(filename):
    # Assuming 'your_package' is your package name
    return app.send_static_file(f'app/{filename}')

from app import admins
from app import attendants