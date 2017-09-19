import logging
import json

from flask.views import MethodView
from flask import request
from flask_login import current_user, login_required

from app import app
from app.models.user import User
from app.controller.events import EventController
from app.constants.error import (JSON_NOT_FOUND_400, START_DATE_NOT_FOUND_400,
                                 END_DATE_NOT_FOUND_400, GROUP_ID_NOT_FOUND_400,
                                 GROUP_NAME_NOT_FOUND_400, EVENT_ID_NOT_FOUND_400)


class EventView(MethodView):
    decorators = [login_required]

    def __init__(self):  # pragma: no cover
        self.control = EventController()

    def post(self):
        logging.info("New POST /event request")
        data = request.get_json()

        if not data:
            return json.dumps(JSON_NOT_FOUND_400), 400
        if not data.get("group_id"):
            return json.dumps(GROUP_ID_NOT_FOUND_400), 400
        if not data.get("name"):
            return json.dumps(GROUP_NAME_NOT_FOUND_400), 400
        if not data.get("start_date"):
            return json.dumps(START_DATE_NOT_FOUND_400), 400
        if not data.get("end_date"):
            return json.dumps(END_DATE_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.create_new_event(current_user, **data)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status

    def patch(self):
        logging.info("New PATCH /event request")
        data = request.get_json()

        if not data:
            return json.dumps(JSON_NOT_FOUND_400), 400
        if not data.get("event_id"):
            return json.dumps(EVENT_ID_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.patch_event_info(current_user, **data)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status

    def get(self):
        logging.info("New GET /event request")
        event_id = request.args.get('event_id')
        if not event_id:
            return json.dumps(EVENT_ID_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.get_event_info(event_id)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status

    def delete(self):
        logging.info("New DELETE /event request")
        data = request.get_json()

        if not data:
            return json.dumps(JSON_NOT_FOUND_400), 400
        if not data.get("event_id"):
            return json.dumps(EVENT_ID_NOT_FOUND_400), 400

        if type(current_user._get_current_object()) is User:
            result, status = self.control.delete_event(current_user, **data)
        else:
            result, status = ("Not logged in", 300)
        return json.dumps(result), status


app.add_url_rule('/event', view_func=EventView.as_view('event'))
