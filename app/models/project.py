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


class BidProject(Base):
    __tablename__ = 'bid_project'
    data = db.column(JSON)



    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, id: Union[int, str]):
        return cls.query.filter_by(id=id).first()


    def get_status(self):
        if self.data.get('recommend_id'):
            return 'finish'
        else:
            return 'undertaking'
    @classmethod
    def get_project_data(cls, project_id: int):
        return cls.get(project_id).data


class BidProjectSchema(marshmallow.Schema):
    # validate
    status = Function(lambda obj: obj.get_status())
    name = Function(lambda obj: obj.data['name'])
    creator = Function(lambda obj: obj.data['name'])
    class Meta:
        fields = ('id', 'name', 'status', 'update_time')

