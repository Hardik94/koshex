import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)


bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


from project.server.auth.view import auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/tiny')

from project.server.auth.start import auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/')
