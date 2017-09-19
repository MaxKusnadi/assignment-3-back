import json

from flask_login import current_user
from app.models.user import User
from app import app, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()


@app.route('/')
def index():
    d = dict()
    if type(current_user._get_current_object()) is User:
        d['text'] = True
        return json.dumps(d)
    d['text'] = False
    return json.dumps(d)
