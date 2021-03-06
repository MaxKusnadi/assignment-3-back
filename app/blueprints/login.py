import requests

from flask import Blueprint, request
from flask_login import login_user, logout_user, login_required

from app.models.user import User
from app.utils import get_or_create
from app.constants.facebook import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
from app import db

auth_bp = Blueprint('auth', __name__)


fb_base_url = 'https://graph.facebook.com/'
fb_app_access_token = None


@auth_bp.route('/login', methods=['POST'])
def login():

    # get app_access_token if we haven't already
    if not fb_app_access_token:
        generate_fb_app_access_token()

    data = request.get_json()

    fb_user_access_token = data.get('user_access_token')
    if valid_fb_user_access_token(fb_user_access_token):
        fb_id = data.get('fb_id')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')

        user, is_new_user = get_or_create(db.session, User, fb_id=fb_id)

        if is_new_user:
            user = User(fb_id, first_name, last_name, email)
            db.session.add(user)
            db.session.commit()

        login_user(user)

        return 'Logged In'

    return 'Error Logging In', 500


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return 'Log out'


# helper functions

def valid_fb_user_access_token(user_access_token):
    debug_user_token_url = '{0}debug_token?input_token={1}&access_token={2}' \
                            .format(fb_base_url, user_access_token, fb_app_access_token)

    r = requests.get(debug_user_token_url).json()
    return r['data']['is_valid']


def generate_fb_app_access_token():
    app_token_url = ('{0}oauth/access_token?client_id={1}&client_secret={2}&grant_type=client_credentials'
                     .format(fb_base_url, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET))
    r = requests.get(app_token_url).json()

    global fb_app_access_token 
    fb_app_access_token = r['access_token']


