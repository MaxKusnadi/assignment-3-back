import logging

from app.scheduler import schedule_event_alert
from app.models.event import Event
from app.models.group import Group
from app.models.attendance import Attendance
from app.models.usergroup import UserGroup
from app.constants.error import (GROUP_NOT_FOUND_404, USER_NOT_GROUP_CREATOR_301,
                                 EVENT_NOT_FOUND_404, EVENT_NOT_FROM_THIS_GROUP_301,
                                 START_DATE_LATER_THAN_END_DATE_400, USER_NOT_IN_GROUP_301,
                                 VERIFICATION_ERROR_301)
from app import db


class EventController:

    def create_new_event(self, user, **kwargs):
        logging.info("Creating a event for user {user_id}".format(user_id=user.id))
        group_id = int(kwargs.get('group_id'))
        name = kwargs.get('name')
        start_date = int(kwargs.get("start_date"))
        end_date = int(kwargs.get("end_date"))
        location = kwargs.get("location", "")
        description = kwargs.get("description", "")
        alert_time = kwargs.get("alert_time")
        alert_time = int(alert_time) if alert_time else None
        verification_code = kwargs.get("verification_code")

        group = Group.query.filter(Group.id == group_id,
                                   Group.is_deleted == False).first()

        if not group:
            e = GROUP_NOT_FOUND_404
            e['text'] = e['text'].format(group_id)
            return e, 404
        if group.creator_id != user.id:
            e = USER_NOT_GROUP_CREATOR_301
            e['text'] = e['text'].format(user_id=user.id, group_id=group_id)
            return e, 301
        if start_date > end_date:
            return START_DATE_LATER_THAN_END_DATE_400, 400

        event = Event(group, name, start_date, end_date, description, location, alert_time, verification_code)

        db.session.add(event)
        db.session.commit()

        if alert_time:
            schedule_event_alert(event)

        attendance = Attendance(user, event, 1, "")
        db.session.add(attendance)
        db.session.commit()

        d = dict()
        d['event_id'] = event.id
        d['name'] = event.name
        d['start_date'] = event.start_date
        d['end_date'] = event.end_date
        d['description'] = event.description
        d['location'] = event.location
        d['alert_time'] = event.alert_time
        d['verification_code'] = event.verification_code

        return d, 200

    def patch_event_info(self, user, event_id, **kwargs):
        logging.info("Patching event {event_id} for user {user_id}".format(event_id=event_id,
                                                                           user_id=user.id))
        name = kwargs.get('name')
        start_date = kwargs.get("start_date")
        start_date = int(start_date) if start_date else None
        end_date = kwargs.get("end_date")
        end_date = int(end_date) if end_date else None
        location = kwargs.get("location")
        description = kwargs.get("description")
        alert_time = kwargs.get("alert_time")
        alert_time = int(alert_time) if alert_time else None
        verification_code = kwargs.get('verification_code')

        event = Event.query.filter(Event.id == event_id,
                                   Event.is_deleted == False).first()

        if not event:
            e = EVENT_NOT_FOUND_404
            e['text'] = e['text'].format(event_id)
            return e, 404

        group_id = event.group_id
        group = Group.query.filter(Group.id == group_id,
                                   Group.is_deleted == False).first()

        if not group:
            e = GROUP_NOT_FOUND_404
            e['text'] = e['text'].format(group_id)
            return e, 404
        if group.creator_id != user.id:
            e = USER_NOT_GROUP_CREATOR_301
            e['text'] = e['text'].format(user_id=user.id, group_id=group_id)
            return e, 301

        if event not in group.events:
            e = EVENT_NOT_FROM_THIS_GROUP_301
            e['text'] = e['text'].format(event_id=event_id, group_id=group_id)
            return e, 301

        start_date = start_date if start_date else event.start_date
        end_date = end_date if end_date else event.end_date

        if start_date > end_date:
            return START_DATE_LATER_THAN_END_DATE_400, 400

        event.name = name if name else event.name
        event.start_date = start_date
        event.end_date = end_date
        event.location = location if location else event.location
        event.description = description if description else event.description
        event.alert_time = alert_time if alert_time else event.alert_time
        event.verification_code = verification_code if verification_code else event.verification_code

        db.session.commit()

        if alert_time:
            schedule_event_alert(event)

        if verification_code:
            attendance = Attendance.query.filter(Attendance.user_id == user.id,
                                                 Attendance.event_id == event_id).first()
            attendance.status = 3
            db.session.commit()

        d = dict()
        d['event_id'] = event.id
        d['name'] = event.name
        d['start_date'] = event.start_date
        d['end_date'] = event.end_date
        d['description'] = event.description
        d['location'] = event.location
        d['verification_code'] = event.verification_code

        return d, 200

    def get_event_info(self, user, event_id):
        event_id = int(event_id)
        logging.info("Getting info for event {event_id}".format(event_id=event_id))
        event = Event.query.filter(Event.id == event_id,
                                   Event.is_deleted == False).first()
        if not event:
            logging.error("Event of id {} is not found".format(event_id))
            e = EVENT_NOT_FOUND_404
            e['text'] = e['text'].format(event_id)
            return e, 404
        # Check if user is admin
        group = Group.query.filter(Group.id == event.group_id).first()
        is_user_admin = False
        if group:
            is_user_admin = group.creator_id == user.id
        d = dict()
        d['event_id'] = event.id
        d['name'] = event.name
        d['start_date'] = event.start_date
        d['end_date'] = event.end_date
        d['description'] = event.description
        d['location'] = event.location
        d['group_id'] = event.group_id
        d['alert_time'] = event.alert_time
        d['has_verification_code'] = True if event.verification_code else False
        if is_user_admin:
            d['verification_code'] = event.verification_code

        return d, 200

    def delete_event(self, user, event_id):
        logging.info("Deleting event {event_id}".format(event_id=event_id))
        event = Event.query.filter(Event.id == event_id,
                                   Event.is_deleted == False).first()
        if not event:
            logging.error("Event of id {} is not found".format(event_id))
            e = EVENT_NOT_FOUND_404
            e['text'] = e['text'].format(event_id)
            return e, 404

        group_id = event.group_id
        group = Group.query.filter(Group.id == group_id,
                                   Group.is_deleted == False).first()

        if not group:
            e = GROUP_NOT_FOUND_404
            e['text'] = e['text'].format(group_id)
            return e, 404
        if group.creator_id != user.id:
            e = USER_NOT_GROUP_CREATOR_301
            e['text'] = e['text'].format(user_id=user.id, group_id=group_id)
            return e, 301

        if event not in group.events:
            e = EVENT_NOT_FROM_THIS_GROUP_301
            e['text'] = e['text'].format(event_id=event_id, group_id=group_id)
            return e, 301

        event.is_deleted = True
        db.session.commit()

        d = dict()
        d['text'] = "Delete successful"

        return d, 200

    def get_user_event(self, user):
        logging.info("Getting all events for user {user_id}".format(user_id=user.id))
        groups = UserGroup.query.filter(UserGroup.user_id == user.id).all()
        groups = list(map(lambda x: Group.query.filter(Group.id == x.group_id,
                                                       Group.is_deleted == False).first(), groups))
        groups = list(filter(lambda x: x, groups))

        events = []
        for group in groups:
            events.extend(group.events)

        events = list(filter(lambda x: x.is_deleted is False, events))

        result = list(map(lambda x:{
            "event_id": x.id,
            "name": x.name,
            "start_date": x.start_date,
            "end_date": x.end_date,
            "description": x.description,
            "location": x.location,
            "alert_time": x.alert_time
        }, events))

        return result, 200

    def get_group_event(self, user, group_id):
        logging.info("Getting all events for group {group_id}".format(group_id=group_id))

        group = Group.query.filter(Group.id == group_id,
                                   Group.is_deleted == False).first()
        if not group:
            logging.error("Group of id {} is not found".format(group_id))
            e = GROUP_NOT_FOUND_404
            e['text'] = e['text'].format(group_id)
            return e, 404

        # Check if the user is the member
        user_group = UserGroup.query.filter(UserGroup.group_id == group_id,
                                            UserGroup.user_id == user.id).first()
        if not user_group:
            logging.error("User of id {} is not member of group {}".format(user.id, group_id))
            e = USER_NOT_IN_GROUP_301
            e['text'] = e['text'].format(user_id=user.id, group_id= group_id)
            return e, 301

        events = group.events
        events = list(filter(lambda x: x.is_deleted is False, events))

        result = list(map(lambda x:{
            "event_id": x.id,
            "name": x.name,
            "start_date": x.start_date,
            "end_date": x.end_date,
            "description": x.description,
            "location": x.location,
            "alert_time": x.alert_time
        }, events))

        return result, 200

    def confirm_attendance(self, user, **kwargs):
        event_id = kwargs.get("event_id")
        verification_code = kwargs.get("verification_code")
        logging.info("Confirming event {event_id} for user {user_id}".format(event_id=event_id,
                                                                             user_id=user.id))
        event = Event.query.filter(Event.id == event_id,
                                   Event.is_deleted == False).first()
        if not event:
            logging.error("Event of id {} is not found".format(event_id))
            e = EVENT_NOT_FOUND_404
            e['text'] = e['text'].format(event_id)
            e['is_code_correct'] = False
            return e, 404

        group_id = event.group_id
        group = Group.query.filter(Group.id == group_id,
                                   Group.is_deleted == False).first()

        if not group:
            e = GROUP_NOT_FOUND_404
            e['text'] = e['text'].format(group_id)
            e['is_code_correct'] = False
            return e, 404

        # Check if the user is the member
        user_group = UserGroup.query.filter(UserGroup.group_id == group_id,
                                            UserGroup.user_id == user.id).first()
        if not user_group:
            logging.error("User of id {} is not member of group {}".format(user.id, group_id))
            e = USER_NOT_IN_GROUP_301
            e['text'] = e['text'].format(user_id=user.id, group_id=group_id)
            e['is_code_correct'] = False
            return e, 301

        if verification_code != event.verification_code:
            logging.error("Verification error for event {event_id} and user {user_id}".format(event_id=event_id,
                                                                                              user_id=user.id))
            e = VERIFICATION_ERROR_301
            e['text'] = e['text'].format(event_id=event_id, user_id=user.id)
            e['is_code_correct'] = False
            return e, 200

        attendance = Attendance.query.filter(Attendance.user_id == user.id,
                                             Attendance.event_id == event_id).first()

        if not attendance:
            attendance = Attendance(user, event, 3, "")
            db.session.add(attendance)
            db.session.commit()
        else:
            attendance.status = 3
            db.session.commit()
        d = dict()
        d['text'] = "Successful"
        d['is_code_correct'] = True
        return d, 200
