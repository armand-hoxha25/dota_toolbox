from flask import Flask
import logging
import os
from config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_folder='static',
            template_folder='static/templates')
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from app import routes, models, errors  # nopep8
