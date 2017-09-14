from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app import db


class UserGroup(db.Model):
    __tablename__ = 'usergroup'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'), primary_key=True)

    user = relationship("User", backref="groups")
    group = relationship("Group", backref="users")

    def __init__(self, user, group):
        self.user = user
        self.group = group
        self.user_id = user.id
        self.group_id = group.id

    def __repr__(self):
        return "User: {user} - Group: {group}".format(user=self.user_id, group=self.group_id)
