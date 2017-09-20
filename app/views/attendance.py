import logging
import json

from flask.views import MethodView
from flask import request
from flask_login import current_user, login_required

from app import app
from app.models.user import User
from app.controller.attendance import AttendanceController
from app.constants.error import (JSON_NOT_FOUND_400, GROUP_ID_NOT_FOUND_400,
                                 EVENT_ID_NOT_FOUND_400, ATTENDANCE_STATUS_NOT_FOUND_400)


class AttendanceView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = AttendanceController()

    def post(self):
        logging.info("New POST /attendance request")
        data = request.get_json()

        if not data:
            return json.dumps(JSON_NOT_FOUND_400), 400
        if not data.get("event_id"):
            return json.dumps(EVENT_ID_NOT_FOUND_400), 400
        if not data.get("status"):
            return json.dumps(ATTENDANCE_STATUS_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.create_new_attendance(current_user, **data)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status

    def patch(self):
        logging.info("New PATCH /attendance request")
        data = request.get_json()

        if not data:
            return json.dumps(JSON_NOT_FOUND_400), 400
        if not data.get("event_id"):
            return json.dumps(EVENT_ID_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.patch_attendance(current_user, **data)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status

    def get(self):
        logging.info("New GET /attendance request")
        event_id = request.args.get('event_id')
        if not event_id:
            return json.dumps(EVENT_ID_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.get_attendance_info(event_id)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status


class MyAttendanceView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = AttendanceController()

    def get(self):
        logging.info("New GET /me/attendance request")
        event_id = request.args.get('event_id')
        if not event_id:
            return json.dumps(EVENT_ID_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.get_my_attendance_info(current_user, event_id)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status


app.add_url_rule('/attendance', view_func=AttendanceView.as_view('attendance'))
app.add_url_rule('/me/attendance', view_func=MyAttendanceView.as_view('me/attendance'))