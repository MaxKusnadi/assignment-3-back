import requests

from flask import Blueprint, redirect, url_for, session, request
from flask_login import login_user, logout_user, login_required

from app.models.user import FBUser, User
from app.utils import get_or_create
from app.constants.facebook import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
from app import db

login_bp = Blueprint('login', __name__)


fb_base_url = 'https://graph.facebook.com/'
fb_app_access_token = None


@login_bp.route('/')
def login():

    # get app_access_token if we haven't already
    if not fb_app_access_token:
        generate_fb_app_access_token()

    fb_user_access_token = request.args.get('user_access_token')
    if valid_fb_user_access_token(fb_user_access_token):
        args = request.args
        fb_id = args.get('fb_id')
        first_name = args.get('first_name')
        last_name = args.get('last_name')
        email = args.get('email')

        fb_user, is_new_user = get_or_create(db.session, FBUser, fb_id=fb_id)

        user = None
        if is_new_user:
            user = User(first_name, last_name, email)
            fb_user.user = user
            db.session.add(user)
            db.session.commit()
        else:
            user = fb_user.user

        login_user(user)

        return 'Logged In'

    return 'BAD', 500


@login_bp.route('/logout')
@login_required
def logout():
    logout_user()


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


