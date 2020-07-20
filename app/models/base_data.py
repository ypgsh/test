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


class ValveProducts(Base):
    __tablename__ = 'valve_product_table'
    model_id = db.column(db.string(128))      #
    model_version = db.column(db.string(128))
    series_id = db.column(db.string(128))
    cad_status = db.column(db.string(128))
    press_class = db.column(db.string(128))
    temp_class = db.column(db.string(128))
    press_design = db.column(db.string(128))
    temp_design = db.column(db.string(128))
    stop_throat_diam = db.column(db.string(128))
    gov_throat_diam = db.column(db.string(128))
    ovld_throat_diam = db.column(db.string(128))
    stop_stem_lift = db.column(db.string(128))
    gov_stem_lift = db.column(db.string(128))
    ovld_stem_lift = db.column(db.string(128))
    shape_id = db.column(db.string(128))
    cv_calc = db.column(db.string(128))
    cv = db.column(db.string(128))
    casing_mat = db.column(db.string(128))
    stem_mat = db.column(db.string(128))
    dim_a = db.column(db.string(128))
    dim_b = db.column(db.string(128))
    dim_c = db.column(db.string(128))
    dim_d = db.column(db.string(128))
    dim_e_l = db.column(db.string(128))
    fluid_mode = db.column(db.string(128))
    gov_mode = db.column(db.string(128))
    install_mode = db.column(db.string(128))
    act_oil_press_mode = db.column(db.string(128))
    eql_roll = db.column(db.string(128))
    out_conn_type = db.column(db.string(128))
    act_conn_type = db.column(db.string(128))
    cost_level = db.column(db.string(128))
    weight_total = db.column(db.string(128))
    industry = db.column(db.string(128))
    dwg_id = db.column(db.string(128))
    turbine_id = db.column(db.string(128))
    description = db.column(db.string(128))
    comments = db.column(db.string(128))
    used = db.column(db.string(128))
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
    unit_run_mode = db.column(db.string(128))
    press_loss_range = db.column(ARRAY(db.float))
    speed_range = db.column(ARRAY(db.float))
    suitable_unit = db.column(db.string(128))
    comments = db.column(db.string(128))

    def delete(self):

        db.session.delete(self)
        db.session.commit()

class ValveSeries(Base):
    code = db.column(db.string(128))
    structure = db.column(db.string(128))
    use_scene = db.column(db.string(128))
    sets = db.column(ARRAY(db.string(32)))
    sketch = db.column(db.text)

class Pressure(Base):
    design_press = db.column(db.float)
    press_range = db.column(ARRAY(db.float))
    update_by = db.column(db.integer)

class Temperature(Base):
    design_temp = db.column(db.float)
    temp_range = db.column(ARRAY(db.float))
    update_by = db.column(db.integer)


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