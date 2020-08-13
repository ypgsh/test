
from app.extension import db

from .base import Base


class User(Base):
    __tablename__ = 'user'
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128))
    office_name = db.Column(db.String(128))
    deleted = db.Column(db.Boolean, default=False)


class UserRole(Base):
    user_id = db.Column(db.String(64))
    role_id = db.Column(db.Integer)


class Roles(Base):
    name = db.Column(db.String(64))