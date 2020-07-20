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


class Forms(Base):
    __tablename__ = 'forms'
    module_name = db.Column(db.String(128))
    page_name = db.Column(db.String(128))
    var_name = db.Column(db.String(128))
    name = db.Column(db.String(128))
    style = db.Column(db.String(32))
    version = db.Column(db.integer)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class FormAttr(Base):
    form_id = db.Column(db.Integer)
    name = db.Column(db.String(128))
    var_name = db.Column(db.String(64))
    symbol = db.Column(db.String(32), default='')
    unit = db.Column(db.String(32), default='')
    value_type = db.Column(db.String(32))
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


class Attribute(Base):
    name = db.Column(db.String(128))
    var_name = db.Column(db.String(64))
    symbol = db.Column(db.String(32), default='')
    unit = db.Column(db.String(32), default='')
    value_type = db.Column(db.String(32))




