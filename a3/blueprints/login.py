from flask import Blueprint, Flask, redirect, url_for, session, request
from flask_login import login_user, logout_user, login_required
from flask_oauth import OAuth
from a3.database import db_session
from a3.models import FBUser, User
from a3.utils import get_or_create


FACEBOOK_APP_ID = '1935737966751741'
FACEBOOK_APP_SECRET = 'fe3f2c94880c643b81e839bdec30e7e1'


oauth = OAuth()
login_bp = Blueprint('login', __name__)


facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)


@login_bp.route('/')
def get_login():
    return facebook.authorize(callback=url_for('login.facebook_authorized',
        next=request.args.get('next') or request.referrer or None,
        _external=True))


@login_bp.route('/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    next = request.args.get('next')
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
        return redirect(next)

    session['oauth_token'] = (resp['access_token'], '')

    fb_id = facebook.get('/me').data['id']
    fb_user, is_new_user = get_or_create(db_session, FBUser, fb_id=fb_id)

    if is_new_user:
        fb_data = facebook.get('/me?fields=first_name,last_name,email').data

        user = User()
        user.first_name = fb_data['first_name']
        user.last_name = fb_data['last_name']
        user.email = fb_data['email']
        fb_user.user = user
        db_session.add(user)
        db_session.commit()
    else:
        user = fb_user.user
    
    login_user(user)

    return redirect(next or url_for('index'))

@login_bp.route('/logout')
@login_required
def logout():
    logout_user()

    if 'oauth_token' in session:
        session.pop('oauth_token')

    return redirect(url_for('index'))

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')
