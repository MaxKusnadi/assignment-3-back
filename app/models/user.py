from flask_login import UserMixin
from sqlalchemy import BigInteger, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app import db


class FBUser(db.Model):
    __tablename__ = 'fb_user'

    id = Column(Integer, primary_key=True)
    fb_id = Column(BigInteger, unique=True)

    user = relationship('User', uselist=False, back_populates='fb_user')
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):  # pragma: no cover
        return '<{id} - {user_id}>'.format(id=self.id, user_id=self.fb_id)


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(80))
    last_name = Column(String(80))
    email = Column(String(80))

    fb_user = relationship('FBUser', uselist=False, back_populates='user')

    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

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

    def __repr__(self):  # pragma: no cover
        return '<User {}_{}>'.format(self.first_name, self.last_name)
