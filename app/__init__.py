from flask import Flask
import logging
import os
from config import Config
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask('dota_toolbox', static_folder='static',
                template_folder='app/static/templates')
    app.config.from_object(Config)
    bootstrap = Bootstrap(app)
    port = int(os.environ.get('PORT', 5000))
    print('PORT SELECTED : ', port)
    #app.run(host='0.0.0.0', port=port)
    print('app is currently running')
    # app.run()
    app.debug = True
    return app
#print('APP INITIALIZED AND RUNNING Port= {}'.format(port))

#from app import routes, models, errors  # nopep8
