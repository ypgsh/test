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

class ProductMixin:
    model_id = db.column(db.string(128))  # 阀门型号
    model_version = db.column(db.string(32))  # 型号版本
    series_id = db.column(db.integer)  # 阀门系列
    cad_status = db.column(db.string(128))  # 模型状态
    press_class = db.column(db.integer)  # 压力等级
    temp_class = db.column(db.integer)  # 温度等级
    design_press = db.column(db.FLOAT)  # 设计压力
    design_temp = db.column(db.FLOAT)  # 设计温度
    shape_id = db.column(db.string(32))  # 型线代号
    casing_mat_name = db.column(db.string(128))  # 气缸材料
    stem_mat_name = db.column(db.string(128))  # 提升杆材料
    fluid_medium_name = db.column(db.string(128))  # 介质
    gov_mode = db.column(db.string(128))  # 配汽方式
    install_mode = db.column(db.string(128))  # 安装固定方式
    act_oil_press_mode = db.column(db.string(128))  # 执行机构油压类型
    pilot_speedup = db.column(db.BOOLEAN)  # 预启阀冲转
    act_conn_type = db.column(db.string(128))  # 执行机构连接方式
    cost_level = db.column(db.string(32))  # 成本
    total_weight = db.column(db.FLOAT)  # 阀门总重
    industry = db.column(db.BOOLEAN)  # 行业（工业透平适用）
    dwg_id = db.column(db.string(128))  # 阀门图号
    turbine_unit_ids = db.column(ARRAY(db.string(64)))  # 机组编号(制造单号)
    description = db.column(db.string(128))  # 特性简介
    comments = db.column(db.string(128))  # 备注
    used = db.column(db.BOOLEAN)  # 是否选型

class ValveProducts(Base, ProductMixin):
    __tablename__ = 'valve_product_table'
    stop_throat_diam = db.column(db.FLOAT)  # 主门口径/主阀喉部直径
    gov_throat_diam = db.column(db.FLOAT)  # 调阀喉部直径
    ovld_throat_diam = db.column(db.FLOAT)  # 补汽阀喉部直径
    stop_stem_lift = db.column(db.FLOAT)  # 主阀阀杆行程
    stop_stem_lift_main = db.column(db.FLOAT)  # 大阀行程
    stop_stem_lift_eql = db.column(db.FLOAT)  # 预启阀行程
    gov_stem_lift = db.column(db.FLOAT)  # 调阀阀杆行程
    ovld_stem_lift = db.column(db.FLOAT)  # 补汽阀阀杆行程
    cv_calc = db.column(db.FLOAT)  # Cv计算值
    cv = db.column(db.FLOAT)  #
    feature_size_a = db.column(db.FLOAT)  # 特征尺寸a
    feature_size_b = db.column(db.FLOAT)  #
    feature_size_c = db.column(db.FLOAT)  #
    feature_size_d = db.column(db.FLOAT)  #
    feature_size_e_l = db.column(db.FLOAT)  #
    out_conn_type = db.column(db.string(128))  # 出口接口形式

    deleted = db.Column(db.Boolean, default=False)

    def delete(self):
        self.extra_info.delete()
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, id: Union[int, str]):
        pass


class ValveProducts58(Base, ProductMixin):
    __tablename__ = 'valve_product_5_8_table'
    equiv_diam = db.column(db.FLOAT)  # 当量口径
    gov_num = db.column(db.integer)  # 调门个数
    lever_num = db.column(db.integer)  # 杠杆个数
    gov_throat_diams = db.column(ARRAY(db.FLOAT))  # 调阀喉部直径
    gov_stem_empty_lifts = db.column(ARRAY(db.FLOAT))  # 调阀空行程
    gov_stem_max_lifts = db.column(ARRAY(db.FLOAT))  # 调阀全开行程
    servo_max_lifts = db.column(ARRAY(db.FLOAT))  # 油动机全开行程
    deleted = db.Column(db.Boolean, default=False)

    def delete(self):
        self.extra_info.delete()
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, id: Union[int, str]):
        pass


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
    id = db.column(db.Integer, unique_key=True)
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
