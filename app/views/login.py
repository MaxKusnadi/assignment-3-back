from flask import render_template
from flask_login import current_user
from app.models.user import User
from app import app, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()


@app.route('/')
def index():
    if type(current_user._get_current_object()) is User:
        return 'Current User authenticated: {}'.format(current_user.first_name)
    return render_template('index.html')
