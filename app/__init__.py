import logging

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


logging.basicConfig(level=logging.INFO,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object('config')
login_manager = LoginManager(app)
db = SQLAlchemy(app)

# Models
from app.models.user import FBUser, User
from app.models.group import Group
from app.models.event import Event
from app.models.usergroup import UserGroup
from app.models.attendance import Attendance

# Views
from app.views.login import *
from app.views.user import *
from app.views.group import *
from app.views.events import *
from app.views.attendance import *
from app.blueprints.login import login_bp
app.register_blueprint(login_bp, url_prefix='/login')

# Scheduler
from app.scheduler import start_scheduler
start_scheduler()
