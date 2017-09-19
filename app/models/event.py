from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app import db


class Event(db.Model):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'))

    name = Column(String(80))
    start_date = Column(Integer)
    end_date = Column(Integer)
    description = Column(Text)
    location = Column(String)
    is_deleted = Column(Boolean)

    group = relationship("Group", backref="events")

    def __init__(self, group, name, start_date, end_date, description, location):
        self.group = group
        self.group_id = group.id

        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.location = location
        self.is_deleted = False

    def __repr__(self):
        return "{id}. Name: {name} is_deleted: {is_deleted} Group: {group_id}".format(
            id=self.id, name=self.name, is_deleted=self.is_deleted, group_id=self.group_id
        )
