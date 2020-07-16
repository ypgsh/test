import os
from typing import Union

from marshmallow.fields import Function, String, DateTime
from marshmallow import validate

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

from flask import current_app

from app.code import ReturnCode
from app.extension import db, marshmallow
from app.models.base import Base

class Project(Base):
    pass

class BidProject(Base):
    __tablename__ = 'bid_project'
    pass

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, id: Union[int, str]):
        return cls.query.filter_by(id=id).first()



