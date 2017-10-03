import logging

from app.models.group import Group
from app.models.usergroup import UserGroup
from app.models.user import User
from app.constants.error import (GROUP_NOT_FOUND_404, USER_NOT_GROUP_CREATOR_301,
                                 USER_NOT_IN_GROUP_301, USER_ALREADY_IN_GROUP_500,
                                 GROUP_NAME_TOO_LONG_500)
from app import db


class GroupController:

    def create_new_group(self, user, **kwargs):
        logging.info("Creating a group for user {user_id}".format(user_id=user.id))
        name = kwargs.get("name")
        if len(name) > 25:
            e = GROUP_NAME_TOO_LONG_500
            return e, 500
        pic_url = kwargs.get("pic_url", "")
        description = kwargs.get("description", "")

        group = Group(user, name, pic_url, description)

        db.session.add(group)
        db.session.commit()

        user_group = UserGroup(user, group)
        db.session.add(user_group)
        db.session.commit()

        d = dict()
        d['group_id'] = group.id
        d['name'] = group.name
        d['pic_url'] = group.pic_url
        d['description'] = group.description
        d['creator_id'] = group.creator_id
        d['creator_fb_id'] = str(user.fb_id)

        return d, 200

    def patch_group_info(self, user, group_id, **kwargs):
        logging.info("Patching group {group_id} for user {user_id}".format(group_id=group_id,
                                                                           user_id=user.id))
        name = kwargs.get("name", "")
        if name:
            if len(name) > 25:
                e = GROUP_NAME_TOO_LONG_500
                return e, 500
        pic_url = kwargs.get("pic_url", "")
        description = kwargs.get("description", "")

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

        group.name = name if name else group.name
        group.pic_url = pic_url if pic_url else group.pic_url
        group.description = description if description else group.description

        db.session.commit()

        d = dict()
        d['group_id'] = group.id
        d['name'] = group.name
        d['pic_url'] = group.pic_url
        d['description'] = group.description
        d['creator_id'] = group.creator_id
        d['creator_fb_id'] = str(user.fb_id)

        return d, 200

    def get_group_info(self, group_id):
        group_id = int(group_id)
        logging.info("Getting info for group {group_id}".format(group_id=group_id))
        group = Group.query.filter(Group.id == group_id,
                                   Group.is_deleted == False).first()
        if not group:
            logging.error("Group of id {} is not found".format(group_id))
            e = GROUP_NOT_FOUND_404
            e['text'] = e['text'].format(group_id)
            return e, 404
        user = User.query.filter(User.id == group.creator_id).first()

        d = dict()
        d['name'] = group.name
        d['pic_url'] = group.pic_url
        d['description'] = group.description
        d['creator_id'] = group.creator_id
        d['creator_fb_id'] = str(user.fb_id)

        return d, 200

    def delete_group(self, user, group_id):
        logging.info("Deleting group {group_id}".format(group_id=group_id))
        group = Group.query.filter(Group.id == group_id,
                                   Group.is_deleted == False).first()
        if not group:
            logging.error("Group of id {} is not found".format(group_id))
            e = GROUP_NOT_FOUND_404
            e['text'] = e['text'].format(group_id)
            return e, 404
        if group.creator_id != user.id:
            logging.error("User {user_id} is not authorized to delete group {group_id}".format(
                user_id=user.id, group_id=group_id
            ))
            e = USER_NOT_GROUP_CREATOR_301
            e['text'] = e['text'].format(user_id=user.id, group_id=group_id)
            return e, 301

        group.is_deleted = True
        db.session.commit()

        d = dict()
        d['text'] = "Delete successful"

        return d, 200

    def get_user_group(self, user):
        logging.info("Getting all groups for user {user_id}".format(user_id=user.id))
        groups = UserGroup.query.filter(UserGroup.user_id == user.id).all()
        groups = list(map(lambda x: Group.query.filter(Group.id == x.group_id,
                                                       Group.is_deleted == False).first(), groups))
        groups = list(filter(lambda x: x, groups))
        result = list(map(lambda x:{
            "group_id": x.id,
            "name": x.name,
            "pic_url": x.pic_url,
            "description": x.description,
            "creator_id": x.creator_id,
            "creator_fb_id": str(User.query.filter(User.id == x.creator_id).first().fb_id)
        }, groups))

        return result, 200

    def join_group(self, user, group_id):
        logging.info("User {user_id} joining group {group_id}".format(user_id=user.id,
                                                                      group_id=group_id))
        group = Group.query.filter(Group.id == group_id,
                                   Group.is_deleted == False).first()
        if not group:
            logging.error("Group of id {} is not found".format(group_id))
            e = GROUP_NOT_FOUND_404
            e['text'] = e['text'].format(group_id)
            return e, 404

        user_group = UserGroup.query.filter(UserGroup.user_id == user.id,
                                            UserGroup.group_id == group.id).first()
        if user_group:
            logging.error("User {} is already in group {}".format(user.id, group_id))
            e = USER_ALREADY_IN_GROUP_500
            e['text'] = e['text'].format(user.id, group_id)
            return e, 200

        user_group = UserGroup(user, group)
        db.session.add(user_group)
        db.session.commit()

        d = dict()
        d['text'] = "User {user_id} joining group {group_id}".format(user_id=user.id,
                                                                     group_id=group_id)
        return d, 200

    def quit_group(self, user, **kwargs):
        group_id = int(kwargs.get("group_id"))
        logging.info("User {user_id} quiting group {group_id}".format(user_id=user.id,
                                                                      group_id=group_id))
        group = Group.query.filter(Group.id == group_id,
                                   Group.is_deleted == False).first()
        if not group:
            logging.error("Group of id {} is not found".format(group_id))
            return GROUP_NOT_FOUND_404.format(group_id), 404

        user_group = UserGroup.query.filter(UserGroup.group_id == group_id,
                                            UserGroup.user_id == user.id).first()

        if not user_group:
            logging.error("User {user_id} is not in group {group_id}".format(user_id=user.id,
                                                                             group_id=group_id))
            e = USER_NOT_IN_GROUP_301
            e['text'] = e['text'].format(user_id=user.id, group_id=group_id)
            return e, 301
        db.session.delete(user_group)
        db.session.commit()

        d = dict()
        d['text'] = "User {user_id} quiting group {group_id}".format(user_id=user.id,
                                                                     group_id=group_id)
        return d, 200
