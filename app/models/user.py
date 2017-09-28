from flask_login import UserMixin
from sqlalchemy import BigInteger, Column, Integer, String, Boolean
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    fb_id = Column(BigInteger, unique=True)
    first_name = Column(String(80))
    last_name = Column(String(80))
    email = Column(String(80))
    phone = Column(String)
    is_deleted = Column(Boolean)

    def __init__(self, fb_id, first_name, last_name, email, phone=""):
        self.fb_id = fb_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.is_deleted = False

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
