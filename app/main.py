
import os

from flask import Flask
from flask_cors import CORS


from app.extension import db, marshmallow

from app.views import auth, function, form, base_dbs
from app.config import get_config

def config_blueprint(app):
    _ = [app.register_blueprint(bp, url_prefix='/api/sec_valve/v1')
    for bp in (auth, function, form, base_dbs)]


def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))
    config_blueprint(app)
    db.init_app(app)
    marshmallow.init_app(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Credentials'] = 'true'
        return response


    return app




if __name__ == '__main__':
   pass