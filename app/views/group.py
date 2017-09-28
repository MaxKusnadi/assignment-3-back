import logging
import json

from flask.views import MethodView
from flask import request
from flask_login import current_user, login_required

from app import app
from app.models.user import User
from app.controller.group import GroupController
from app.constants.error import JSON_NOT_FOUND_400, GROUP_NAME_NOT_FOUND_400, GROUP_ID_NOT_FOUND_400


class GroupView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = GroupController()

    def post(self):
        logging.info("New POST /group request")
        data = request.get_json()

        if not data:
            return json.dumps(JSON_NOT_FOUND_400), 400
        if not data.get("name"):
            return json.dumps(GROUP_NAME_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.create_new_group(current_user, **data)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status

    def patch(self):
        logging.info("New PATCH /group request")
        data = request.get_json()

        if not data:
            return json.dumps(JSON_NOT_FOUND_400), 400
        if not data.get("group_id"):
            return json.dumps(GROUP_ID_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.patch_group_info(current_user, **data)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status

    def get(self, group_id):
        logging.info("New GET /group request")
        if not group_id:
            return json.dumps(GROUP_ID_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.get_group_info(group_id)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status

    def delete(self):
        logging.info("New DELETE /group request")
        data = request.get_json()

        if not data:
            return json.dumps(JSON_NOT_FOUND_400), 400
        if not data.get("group_id"):
            return json.dumps(GROUP_ID_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.delete_group(current_user, **data)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status


class MyGroupView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = GroupController()

    def get(self):
        logging.info("New GET /me/group request")

        if type(current_user._get_current_object()) is User:
            result, status = self.control.get_user_group(current_user)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status

    def post(self):
        logging.info("New POST /me/group request")
        data = request.get_json()

        if not data:
            return json.dumps(JSON_NOT_FOUND_400), 400
        if not data.get("group_id"):
            return json.dumps(GROUP_ID_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.join_group(current_user, **data)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status

    def delete(self):
        logging.info("New DELETE /me/group request")
        data = request.get_json()

        if not data:
            return json.dumps(JSON_NOT_FOUND_400), 400
        if not data.get("group_id"):
            return json.dumps(GROUP_ID_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.quit_group(current_user, **data)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status


class JoinGroupView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = GroupController()

    def get(self, group_id):
        logging.info("New GET /join/group request")
        if not group_id:
            return json.dumps(GROUP_ID_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.join_group(current_user, group_id)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status


app.add_url_rule('/group', view_func=GroupView.as_view('group'), methods=['POST', 'PATCH', 'DELETE'])
app.add_url_rule('/group/<int:group_id>', view_func=GroupView.as_view('group'), methods=['GET'])
app.add_url_rule('/me/group', view_func=MyGroupView.as_view('my_group'))
app.add_url_rule('/join/group/<int:group_id>', view_func=MyGroupView.as_view('join_group'))
