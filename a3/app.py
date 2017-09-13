from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from a3.blueprints.login import login_bp
from a3.models import User


app = Flask(__name__)
app.secret_key = 'secret key'
app.register_blueprint(login_bp, url_prefix='/login')

login_manager = LoginManager(app)
login_manager.login_view = 'login.get_login'


@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id).first()


@app.route('/')
def index():
    if type(current_user._get_current_object()) is User:
        return 'Current User authenticated: {}'.format(current_user.first_name)
    return render_template('index.html')


@app.cli.command()
def init_db():
    ''' Initialize the database. '''

    from a3.database import init_db
    init_db()
