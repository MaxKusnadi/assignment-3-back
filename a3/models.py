from datetime import datetime, timedelta
from flask_login import UserMixin
from sqlalchemy import BigInteger, Column, Date, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from a3.database import Base

class FBUser(Base):
    __tablename__ = 'fb_user'

    id = Column(Integer, primary_key=True)
    fb_id = Column(BigInteger)

    user = relationship('User', uselist=False, back_populates='fb_user')
    user_id = Column(Integer, ForeignKey('user.id'))


class User(UserMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(80))
    last_name = Column(String(80))
    email = Column(String(80))

    fb_user = relationship('FBUser', uselist=False, back_populates='user')


    def is_active(self):
        """True, as all users are active."""
        return True


    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id


    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True


    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


    def __repr__(self):
        return '<User {}_{}>'.format(self.first_name, self.last_name)
