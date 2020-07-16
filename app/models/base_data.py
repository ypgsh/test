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


class ValveProducts(Base):
    __tablename__ = 'valve_product_table'

    deleted = db.Column(db.Boolean, default=False)
    def delete(self):
        self.extra_info.delete()
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, id: Union[int, str]):
        if isinstance(id, (int, )):
            return cls.query.filter_by(id=id).first()
        elif isinstance(id, (str, )):
            return cls.query.filter_by(tid=id).first()
        else:
            raise Exception('unsupported id type')


class Speed(Base):

    __tablename__ = 'speed_table'




    def delete(self):

        db.session.delete(self)
        db.session.commit()

class ValveSeries(Base):
    pass

class Pressure(Base):
    pass

class Temperature(Base):
    pass

class ValveProductSchema(marshmallow.Schema):
    # validate
    project_code = String(validate=validate.Length(max=128), required=True)
    type = String(validate=validate.Length(max=32), required=True)

    # transform
    id = Function(lambda obj: obj.tid)
    creator_name = Function(lambda obj: obj.creator_id)
    create_time = DateTime()

    class Meta:
        fields = ('id', 'name', 'project_code', 'type', 'version', 'office_name', 'creator_name', 'create_time')