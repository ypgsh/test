import os
from typing import Union
from itertools import chain
from marshmallow.fields import Function, String, DateTime, List
from marshmallow import validate

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

from flask import current_app

from app.code import ReturnCode
from app.extension import db, marshmallow
from app.models.base import Base


class Functions(Base):
    __tablename__ = 'functions'
    name = db.Column(db.String(128), unique=True)
    desc = db.Column(db.String(128))
    input_args = db.Column(ARRAY(db.String(32)))
    code_content = db.Column(db.TEXT)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, name: str):
        return cls.query.filter_by(name=name).first()


    @classmethod
    def get_function_names(cls) -> list:
        function_names_tuples = cls.query.with_entities(cls.name).all()
        function_names_list = list(chain(*function_names_tuples))

        return function_names_list

    @classmethod
    def add_record(cls,
                   name: str,
                   input_args: list,
                   code_content: str,
                   desc: str
                   ) -> Base:
        function_obj = cls(
            name=name,
            input_args=input_args,
            code_content=code_content,
            desc=desc
            ).save()
        assert isinstance(function_obj, (Base,))
        return function_obj

    @classmethod
    def update_record(cls,
                      name: str,
                      **kwargs
                      ):
        invalid_keys = set(kwargs.keys()).difference({'input_args', 'code_content', 'desc'})
        if invalid_keys:
            _ = [kwargs.pop(key) for key in invalid_keys]
        _ = cls.get(name).update(**kwargs)




class FunctionsSchema(marshmallow.Schema):
    # validate
    name = String(validate=validate.Length(max=128), required=True)
    desc = String(validate=validate.Length(max=128), required=True)
    input_args = List(String, required=True)


    # transform
    #
    # creator_name = Function(lambda obj: obj.creator_id)
    # create_time = DateTime()

    class Meta:
        fields = ('name', 'desc', 'input_args', 'code_content')
