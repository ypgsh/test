import os
from typing import Union

from marshmallow.fields import Function, String, DateTime
from marshmallow import validate

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON, ARRAY

from flask import current_app

from app.code import ReturnCode
from app.extension import db, marshmallow
from app.models.base import Base

class ProjectMixin:
    name = db.column(db.string(128))
    creator = db.column(db.integer)

class BidProject(Base, ProjectMixin):
    __tablename__ = 'bid_project'
    status = db.column(db.string(32))
    director = db.column(db.integer)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, id: Union[int, str]):
        return cls.query.filter_by(id=id).first()

class BidProjectInfo(Base):
    __tablename__ = 'bid_project_info'
    project_id = db.column(db.integer)
    data = db.column(JSON)
    result = db.Column(JSON) #{"model_id":"", "comments": ""}

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, id: Union[int, str]):
        return cls.query.filter_by(id=id).first()



