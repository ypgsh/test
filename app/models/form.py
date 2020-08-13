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


class Form(Base):
    __tablename__ = 'form'
    module_name = db.Column(db.String(128))
    page_name = db.Column(db.String(128))
    name = db.Column(db.String(128))
    cn_name = db.Column(db.String(128))
    style = db.Column(db.String(32))
    version = db.Column(db.Integer)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def add_record(cls,
                   module_name: str,
                   page_name: str,
                   name: str,
                   cn_name: str,
                   style: str,
                   version: int = 1
                   ) -> Base:
        form_obj = cls(
            module_name=module_name,
            page_name=page_name,
            name=name,
            cn_name=cn_name,
            style=style,
            version=version
            ).save()
        return form_obj

    @classmethod
    def get_forms(cls, module_name: str, page_name: str):
        form_obj = cls.query.filter_by(module_name=module_name, page_name=page_name).all()
        return form_obj

class FormAttr(Base):
    form_id = db.Column(db.Integer, db.ForeignKey('form.id'))
    attr_id= db.Column(db.Integer, db.ForeignKey('attribute.id'))
    input = db.Column(JSON)  # {input_from: table,table_name:abc, display_field:["abc"], select_field:"abc", addition_value:[{"var_name":def, select_field:def}]}
                                 # {input_from: func}
                                 # {input_from: expression, expression: "3.14*{abc}"}
                                 # {input_from: user_input}
                                 # {input_from: auto_fill}
    performance = db.Column(JSON)    #hide : true # 可见
                                    # widget:  # drop_list / input /PopupWindow
                                    # editable: true # 状态

                                    # update_trigger =  # auto/user_click
                                    # validate = db.Column(JSON) #{constrain: {min:0, max: 120}, alert: PopupWindow}
    dependent_attrs = db.Column(ARRAY(db.String(64)))
    comments = db.Column(db.String(128))

    @classmethod
    def add_record(cls,
                    form_id: int,
                    attr_id: int,
                    input: dict,
                    performance: dict,
                    dependent_attrs: dict,
                    comments: dict = ''
                   ):
        form_attr_obj = cls(
                    form_id=form_id,
                    attr_id=attr_id,
                    input=input,
                    performance=performance,
                    dependent_attrs=dependent_attrs,
                    comments=comments
        ).save()
        return form_attr_obj

    @classmethod
    def get_form_attrs(cls, form_id: int) -> list:
        form_attr_objs = cls.query.filter_by(form_id=form_id).all()
        return form_attr_objs

    @classmethod
    def update_record(cls, id: int, **kwargs):
        invalid_keys = set(kwargs.keys()).difference({'input', 'performance', 'dependent_attrs', 'comments'})
        if invalid_keys:
            _ = [kwargs.pop(key) for key in invalid_keys]
        _ = cls.get(id).update(**kwargs)

class Attribute(Base):
    cn_name = db.Column(db.String(128))
    name = db.Column(db.String(64))
    symbol = db.Column(db.String(32), default='')
    unit = db.Column(db.String(32), default='')
    value_type = db.Column(db.String(32))

    form_attr = relationship("FormAttr", backref="attr")

    @classmethod
    def add_record(cls,
                    cn_name: str,
                    name: str,
                    symbol: str,
                    unit: str,
                    value_type: str
                   ) -> Base:
        attr_obj = cls(
                cn_name=cn_name,
                name=name,
                symbol=symbol,
                unit=unit,
                value_type=value_type
        ).save()
        return attr_obj

    @classmethod
    def get_records(cls, **kwargs) -> list:
        attr_objs = cls.query.filter_by(**kwargs).all()
        return attr_objs

    @classmethod
    def update_record(cls, id: int, **kwargs):
        invalid_keys = set(kwargs.keys()).difference({'cn_name', 'symbol', 'unit', 'value_type'})
        if invalid_keys:
            _ = [kwargs.pop(key) for key in invalid_keys]
        _ = cls.get(id).update(**kwargs)


class AttributeSchema(marshmallow.Schema):
    # validate
    cn_name = String(validate=validate.Length(max=128), required=True)
    name = String(validate=validate.Length(max=64), required=True)
    symbol = String(validate=validate.Length(max=32))
    desc = String(validate=validate.Length(max=32))
    unit = String(validate=validate.Length(max=32))

    class Meta:
        fields = ('id','cn_name', 'name', 'symbol', 'desc', 'unit')

class FormAttrSchema(marshmallow.Schema):
    # validate

    class Meta:
        fields = ('id','form_id', 'attr_id', 'input', 'performance', 'dependent_attrs', 'comments')

class FormSchema(marshmallow.Schema):

    class Meta:
        fields = ('id', 'cn_name', 'name', 'style', 'version', 'module_name', 'page_name')
