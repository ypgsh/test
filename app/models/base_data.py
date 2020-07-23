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
    model_version = db.column(db.string(32))
    series_id = db.column(db.integer)
    cad_status = db.column(db.string(128))
    press_class = db.column(db.integer)
    temp_class = db.column(db.integer)
    press_design = db.column(db.FLOAT)
    temp_design = db.column(db.FLOAT)
    stop_throat_diam = db.column(db.FLOAT)
    gov_throat_diam = db.column(db.FLOAT)
    ovld_throat_diam = db.column(db.FLOAT)
    stop_stem_lift = db.column(db.FLOAT)
    stop_stem_lift_main = db.column(db.FLOAT)
    stop_stem_lift_eql = db.column(db.FLOAT)
    gov_stem_lift = db.column(db.FLOAT)
    ovld_stem_lift = db.column(db.FLOAT)
    shape_id = db.column(db.string(32))
    cv_calc = db.column(db.FLOAT)
    cv = db.column(db.FLOAT)
    casing_mat_name = db.column(db.string(128))
    stem_mat_name = db.column(db.string(128))
    feature_size_a = db.column(db.FLOAT)
    feature_size_b = db.column(db.FLOAT)
    feature_size_c = db.column(db.FLOAT)
    feature_size_d = db.column(db.FLOAT)
    feature_size_e_l = db.column(db.FLOAT)
    fluid_medium_name = db.column(db.string(128))
    gov_mode = db.column(db.string(128))
    install_mode = db.column(db.string(128))
    act_oil_press_mode = db.column(db.string(128))
    pilot_speedup = db.column(db.BOOLEAN)
    out_conn_type = db.column(db.string(128))
    act_conn_type = db.column(db.string(128))
    cost_level = db.column(db.string(32))
    total_weight = db.column(db.FLOAT)
    industry = db.column(db.BOOLEAN)
    dwg_id = db.column(db.string(128))
    turbine_unit_ids = db.column(ARRAY(db.string(64)))
    description = db.column(db.string(128))
    comments = db.column(db.string(128))
    used = db.column(db.BOOLEAN)
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
    suitable_turbine_unit = db.column(db.string(128))
    comments = db.column(db.string(128))

    def delete(self):

        db.session.delete(self)
        db.session.commit()

class ValveSeries(Base):
    code = db.column(db.string(128))
    structure = db.column(db.string(128))
    use_scene = db.column(db.string(128))
    typical_turbine_units = db.column(ARRAY(db.string(32)))
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
    pass
