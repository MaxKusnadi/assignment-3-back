import logging

from app.models.event import Event
from app.models.attendance import Attendance
from app.models.group import Group
from app.models.usergroup import UserGroup
from app.models.user import User
from app.constants.error import (GROUP_NOT_FOUND_404, ATTENDANCE_NOT_FOUND_404,
                                 EVENT_NOT_FOUND_404, USER_NOT_IN_GROUP_301)
from app import db


class AttendanceController:

    def create_new_attendance(self, user, **kwargs):
        logging.info("Creating an attendance for user {user_id}".format(user_id=user.id))
        event_id = int(kwargs.get('event_id'))
        status = int(kwargs.get('status'))
        remark = kwargs.get('remark', "")

        # Check whether the event exists
        event = Event.query.filter(Event.id == event_id,
                                   Event.is_deleted == False).first()
        if not event:
            logging.error("Event of id {} is not found".format(event_id))
            e = EVENT_NOT_FOUND_404
            e['text'] = e['text'].format(event_id)
            return e, 404

        # Check if group still exists
        group_id = event.group_id
        group = Group.query.filter(Group.id == group_id,
                                   Group.is_deleted == False).first()

        if not group:
            e = GROUP_NOT_FOUND_404
            e['text'] = e['text'].format(group_id)
            return e, 404

        # Check if user is member of the group
        user_group = UserGroup.query.filter(UserGroup.user_id == user.id,
                                            UserGroup.group_id == group_id).first()
        if not user_group:
            e = USER_NOT_IN_GROUP_301
            e['text'] = e['text'].format(user_id=user.id, group_id=group_id)
            return e, 301

        attendance = Attendance(user, event, status, remark)
        db.session.add(attendance)
        db.session.commit()

        d = dict()
        d['text'] = "Successful"
        return d, 200

    def patch_attendance(self, user, **kwargs):
        logging.info("Patching an attendance for user {user_id}".format(user_id=user.id))
        event_id = int(kwargs.get('event_id'))
        status = int(kwargs.get('status'))
        remark = kwargs.get('remark')

        # Check whether the event exists
        event = Event.query.filter(Event.id == event_id,
                                   Event.is_deleted == False).first()
        if not event:
            logging.error("Event of id {} is not found".format(event_id))
            e = EVENT_NOT_FOUND_404
            e['text'] = e['text'].format(event_id)
            return e, 404

        # Check if group still exists
        group_id = event.group_id
        group = Group.query.filter(Group.id == group_id,
                                   Group.is_deleted == False).first()

        if not group:
            e = GROUP_NOT_FOUND_404
            e['text'] = e['text'].format(group_id)
            return e, 404

        # Check if user is member of the group
        user_group = UserGroup.query.filter(UserGroup.user_id == user.id,
                                            UserGroup.group_id == group_id).first()
        if not user_group:
            e = USER_NOT_IN_GROUP_301
            e['text'] = e['text'].format(user_id=user.id, group_id=group_id)
            return e, 301

        # Check attendance
        attendance = Attendance.query.filter(Attendance.user_id == user.id,
                                             Attendance.event_id == event_id).first()

        if not attendance:
            e = ATTENDANCE_NOT_FOUND_404
            e['text'] = e['text'].format(user_id=user.id, event_id=event_id)
            return e, 404

        attendance.status = status if status else attendance.status
        attendance.remark = remark if remark else attendance.remark

        db.session.commit()

        d = dict()
        d['text'] = "Successful"
        return d, 200

    def get_attendance_info(self, event_id):
        logging.info("Getting all attendance for event {event_id}".format(event_id=event_id))

        # Check whether the event exists
        event = Event.query.filter(Event.id == event_id,
                                   Event.is_deleted == False).first()
        if not event:
            logging.error("Event of id {} is not found".format(event_id))
            e = EVENT_NOT_FOUND_404
            e['text'] = e['text'].format(event_id)
            return e, 404

        # Check if group still exists
        group_id = event.group_id
        group = Group.query.filter(Group.id == group_id,
                                   Group.is_deleted == False).first()

        if not group:
            e = GROUP_NOT_FOUND_404
            e['text'] = e['text'].format(group_id)
            return e, 404

        # Getting all members of this group
        members = UserGroup.query.filter(UserGroup.group_id == group_id).all()
        members = list(map(lambda x: User.query.filter(User.id == x.user_id).first(), members))

        members_indicate = Attendance.query.filter(Attendance.event_id == event_id).all()
        result = list(map(lambda x: {
            "user_id": x.user_id,
            "status": x.status,
            "name": User.query.filter(User.id == x.user_id).first().first_name
        }, members_indicate))

        members_indicate_id = list(map(lambda x: x.user_id, members_indicate))
        not_respond_members = list(filter(lambda x: x.id not in members_indicate_id, members))
        result_2 = list(map(lambda x: {
            "user_id": x.id,
            "status": 0,
            "name": x.name
        }, not_respond_members))
        result.extend(result_2)
        return result, 200

    def get_my_attendance_info(self, user, event_id):
        logging.info("Getting my attendance for event {event_id}".format(event_id=event_id))

        # Check whether the event exists
        event = Event.query.filter(Event.id == event_id,
                                   Event.is_deleted == False).first()
        if not event:
            logging.error("Event of id {} is not found".format(event_id))
            e = EVENT_NOT_FOUND_404
            e['text'] = e['text'].format(event_id)
            return e, 404

        # Check if group still exists
        group_id = event.group_id
        group = Group.query.filter(Group.id == group_id,
                                   Group.is_deleted == False).first()

        if not group:
            e = GROUP_NOT_FOUND_404
            e['text'] = e['text'].format(group_id)
            return e, 404

        # Check if user is member of the group
        user_group = UserGroup.query.filter(UserGroup.user_id == user.id,
                                            UserGroup.group_id == group_id).first()
        if not user_group:
            e = USER_NOT_IN_GROUP_301
            e['text'] = e['text'].format(user_id=user.id, group_id=group_id)
            return e, 301

        attendance = Attendance.query.filter(Attendance.user_id == user.id,
                                             Attendance.event_id == event_id).first()

        status = attendance.status if attendance else 0

        d = dict()
        d['status'] = status

        return d, 200