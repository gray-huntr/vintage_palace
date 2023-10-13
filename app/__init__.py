from flask import Flask

import configs

app = Flask(__name__)
app.config.from_object(configs.Config)

from app import admins