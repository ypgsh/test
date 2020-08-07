
import os
import json
import shutil
import logging
from typing import Optional

from flask import current_app

from app.views.utils import ReturnCode
from app.models.form import Form, Attribute, FormAttr, AttributeSchema, FormAttrSchema, FormSchema


class FormManager:
    db = Form
    attr_db = FormAttr

    @classmethod
    def create_form(cls, **kwargs) -> tuple:
        form_obj = cls.db.add_record(**kwargs)
        if form_obj is not None:
            return ReturnCode.SUCCESS, form_obj.id
        else:
            return ReturnCode.FAILURE, ''

    @classmethod
    def get_forms(cls, module_name: str, page_name: str) -> tuple:
        form_objs = cls.db.get_forms(module_name, page_name)
        return ReturnCode.SUCCESS, FormSchema().dump(form_objs, many=True)

    @classmethod
    def add_attr(cls, **kwargs):
        form_attr_obj = cls.attr_db.add_record(**kwargs)
        if form_attr_obj is not None:
            return ReturnCode.SUCCESS, form_attr_obj.id
        else:
            return ReturnCode.FAILURE, ''

    @classmethod
    def modify_attr(cls, form_attr_id: int, **kwargs):
        pass


    @classmethod
    def get_form_brief_attrs(cls, form_id: int):
        form_attr_objs = cls.attr_db.get_form_attrs(form_id)
        data = [dict(
                     id=form_attr_obj.id,
                     name=form_attr_obj.attr.name,
                     cn_name=form_attr_obj.attr.cn_name
                    )
                for form_attr_obj in form_attr_objs]
        return ReturnCode.SUCCESS, data

    @classmethod
    def get_form_attr(cls, form_attr_id: int):
        form_attr_obj = cls.attr_db.get(form_attr_id)
        result = FormAttrSchema().dump(form_attr_obj)
        return ReturnCode.SUCCESS, result

    @classmethod
    def modify_form_attr(cls, form_attr_id: int, **kwargs):
        _ = cls.attr_db.update_record(form_attr_id, **kwargs)


class AttributeManager:
    db = Attribute

    @classmethod
    def create_attribute(cls, **kwargs):
        attr_obj = cls.db.add_record(**kwargs)
        if isinstance(attr_obj, cls.db):
            return ReturnCode.SUCCESS, attr_obj.id
        else:
            return ReturnCode.FAILURE, attr_obj

    @classmethod
    def get_attributes(cls, **kwargs):
        attr_objs = cls.db.get_records()
        return ReturnCode.SUCCESS, AttributeSchema().dump(attr_objs, many=True)

    @classmethod
    def modify_attr(cls, attr_id: int, **kwargs):
        _ = cls.db.update_record(attr_id, **kwargs)
        return ReturnCode.SUCCESS, ''

