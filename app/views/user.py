import logging
import json

from flask.views import MethodView
from flask import request
from flask_login import current_user, login_required

from app import app
from app.models.user import User
from app.controller.user import UserController
from app.constants.error import JSON_NOT_FOUND_400, USER_ID_NOT_FOUND_400


class MyInfoView(MethodView):
    decorators = [login_required]

    def __init__(self):
        self.control = UserController()

    def get(self):
        logging.info("New GET /me request")
        if type(current_user._get_current_object()) is User:
            result, status = self.control.get_my_info(current_user)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status

    def patch(self):
        logging.info("New PATCH /me request")
        data = request.get_json()

        if not data:
            return json.dumps(JSON_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.patch_my_info(current_user, **data)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status

    def delete(self):
        logging.info("New DELETE /me request")
        return ""


class UserView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = UserController()

    def get(self):
        logging.info("New GET /user request")
        user_id = request.args.get('user_id')
        if not user_id:
            return json.dumps(USER_ID_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.get_user_info(user_id)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status


app.add_url_rule('/me', view_func=MyInfoView.as_view('my_info'))
app.add_url_rule('/user', view_func=UserView.as_view('user'))
