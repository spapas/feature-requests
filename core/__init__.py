import os
from flask import Flask
from .database import db_session


app = Flask(__name__)
app.secret_key = 'this is a super secret key !!! cool :) 1212222331'


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


import core.views
