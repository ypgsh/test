import os
from typing import Union

from marshmallow.fields import Function, String, DateTime
from marshmallow import validate

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

from flask import current_app

from app.code import ReturnCode
from app.extension import db, marshmallow
from app.models.base import Base


class Functions(Base):
    __tablename__ = 'functions'
    name = db.Column(db.String(128))
    desc = db.Column(db.String(128))
    input_args = db.Column(ARRAY(db.String(32)))
    code_content = db.Column(db.TEXT)

    def delete(self):
        self.extra_info.delete()
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, id: Union[int, str]):
        return cls.query.filter_by(id=id).first()
