import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('core.default_settings')
app.config.from_envvar('LOCAL_SETTINGS')
db = SQLAlchemy(app)
migrate = Migrate(app, db)



import core.views
