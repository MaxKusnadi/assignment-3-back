from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app import db


class Group(db.Model):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey('user.id'))

    name = Column(String(80))
    pic_url = Column(String)
    description = Column(Text)
    is_deleted = Column(Boolean)

    creator = relationship("User", backref="groups_created")

    def __init__(self, creator, name, pic_url, description):
        self.name = name
        self.pic_url = pic_url
        self.description = description
        self.is_deleted = False
        self.creator = creator
        self.creator_id = creator.id

    def __repr__(self):
        return "{id}. Name: {name} is_deleted: {is_deleted} Creator: {creator_id}".format(
            id=self.id, name=self.name, is_deleted=self.is_deleted, creator_id=self.creator_id
        )
