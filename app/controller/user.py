import logging

from app.models.user import User
from app.constants.error import USER_NOT_FOUND_404
from app import db


class UserController:

    def get_my_info(self, user):
        logging.info("Getting the info of user {user_id}".format(user_id=user.id))
        d = dict()
        d['first_name'] = user.first_name
        d['last_name'] = user.last_name
        d['email'] = user.email
        d['fb_id'] = user.fb_user.fb_id
        d['phone'] = user.phone

        return d, 200

    def patch_my_info(self, user, **kwargs):
        logging.info("Updating the info of user {user_id}".format(user_id=user.id))
        email = kwargs.get("email")
        first_name = kwargs.get("first_name")
        last_name = kwargs.get("last_name")
        phone = kwargs.get("phone")

        user.email = email if email else user.email
        user.first_name = first_name if first_name else user.first_name
        user.last_name = last_name if last_name else user.last_name
        user.phone = phone if phone else user.phone

        db.session.commit()

        d = dict()
        d['first_name'] = user.first_name
        d['last_name'] = user.last_name
        d['email'] = user.email
        d['fb_id'] = user.fb_user.fb_id
        d['phone'] = phone

        return d, 200

    def get_user_info(self, user_id):
        user_id = int(user_id)
        user = User.query.filter(User.id == user_id).first()
        if not user:
            e = USER_NOT_FOUND_404
            e['text'] = e['text'].format(user_id)
            return e, 404

        d = dict()
        d['first_name'] = user.first_name
        d['last_name'] = user.last_name
        d['email'] = user.email
        d['fb_id'] = user.fb_user.fb_id
        d['phone'] = user.phone

        return d, 200
