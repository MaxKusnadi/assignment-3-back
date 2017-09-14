from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app import db


class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    event_id = Column(Integer, ForeignKey('event.id'))

    status = Column(Integer)
    remark = Column(String)

    user = relationship("User", backref="attendance")
    event = relationship("Event", backref="users")

    def __init__(self, user, event, status=0, remark=""):
        self.user = user
        self.user_id = user.id

        self.event = event
        self.event_id = event.id

        self.status = status
        self.remark = remark

    def __repr__(self):
        return "User: {user} - Event: {event} - Status: {status}".format(user=self.user_id, event=self.event_id,
                                                                         status=self.status)
