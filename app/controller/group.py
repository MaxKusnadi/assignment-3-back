import logging

from app.models.group import Group
from app.models.usergroup import UserGroup
from app.constants.error import GROUP_NOT_FOUND_404, USER_NOT_GROUP_CREATOR_301
from app import db


class GroupController:

    def create_new_group(self, user, **kwargs):
        logging.info("Creating a group for user {user_id}".format(user_id=user.id))
        name = kwargs.get("name")
        pic_url = kwargs.get("pic_url", "")
        description = kwargs.get("description", "")

        group = Group(user, name, pic_url, description)

        db.session.add(group)
        db.session.commit()

        d = dict()
        d['group_id'] = group.id
        d['name'] = group.name
        d['pic_url'] = group.pic_url
        d['description'] = group.description
        return d, 200

    def patch_group_info(self, user, **kwargs):
        logging.info("Creating a group for user {user_id}".format(user_id=user.id))
        group_id = kwargs.get("group_id")
        name = kwargs.get("name", "")
        pic_url = kwargs.get("pic_url", "")
        description = kwargs.get("description", "")

        group = Group.query.filter(Group.id == group_id).first()

        if not group:
            return GROUP_NOT_FOUND_404.format(group_id), 404
        if group.creator_id != user.id:
            return USER_NOT_GROUP_CREATOR_301.format(user_id=user.id,
                                                     group_id=group_id), 301

        group.name = name if name else group.name
        group.pic_url = pic_url if pic_url else group.pic_url
        group.description = description if description else group.description

        db.session.commit()

        d = dict()
        d['group_id'] = group.id
        d['name'] = group.name
        d['pic_url'] = group.pic_url
        d['description'] = group.description
        return d, 200

    def get_group_info(self, group_id):
        logging.info("Getting info for group {group_id}".format(group_id=group_id))
        group = Group.query.filter(Group.id == group_id,
                                   Group.is_deleted == False).first()
        if not group:
            logging.error("Group of id {} is not found".format(group_id))
            return GROUP_NOT_FOUND_404.format(group_id), 404

        d = dict()
        d['name'] = group.name
        d['pic_url'] = group.pic_url
        d['description'] =  group.description

        return d, 200

    def delete_group(self, user, **kwargs):
        group_id = kwargs.get("group_id")
        logging.info("Deleting group {group_id}".format(group_id=group_id))
        group = Group.query.filter(Group.id == group_id,
                                   Group.is_deleted == False).first()
        if not group:
            logging.error("Group of id {} is not found".format(group_id))
            return GROUP_NOT_FOUND_404.format(group_id), 404
        if group.creator_id != user.id:
            logging.error("User {user_id} is not authorized to delete group {group_id}".format(
                user_id=user.id, group_id=group_id
            ))
            return USER_NOT_GROUP_CREATOR_301.format(user_id=user.id,
                                                     group_id=group_id), 301
        group.is_deleted = True
        db.session.commit()

        d = dict()
        d['text'] = "Delete successful"

        return d, 200

    def get_user_group(self, user):
        logging.info("Getting all groups for user {user_id}".format(user_id=user.id))
        groups = UserGroup.query.filter(UserGroup.user_id == user.id).all()
        result = list(map(lambda x:{
            "group_id": x.id,
            "name": x.name
        }, groups))

        return result, 200

    def join_group(self, user, **kwargs):
        group_id = kwargs.get("group_id")
        logging.info("User {user_id} joining group {group_id}".format(user_id=user.id,
                                                                      group_id=group_id))
        group = Group.query.filter(Group.id == group_id,
                                   Group.is_deleted == False).first()
        if not group:
            logging.error("Group of id {} is not found".format(group_id))
            return GROUP_NOT_FOUND_404.format(group_id), 404

        user_group = UserGroup(user, group)
        db.session.add(user_group)
        db.session.commit()

        d = dict()
        d['text'] = "Delete successful"

        return d, 200
