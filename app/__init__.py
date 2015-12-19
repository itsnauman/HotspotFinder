from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps

import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI') or db_path
app.config["NUM_OF_HOTSPOTS"] = 8 # Num of markers on the map

# Flask extension init
db = SQLAlchemy(app)
GoogleMaps(app)

from . import controller
from . import models
from . import utils
