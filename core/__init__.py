import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('core.default_settings')
app.config.from_pyfile('local.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


import core.views
