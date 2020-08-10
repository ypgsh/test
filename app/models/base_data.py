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
    model_id = db.Column(db.String(128))  # 阀门型号
    model_version = db.Column(db.String(32))  # 型号版本
    series_id = db.Column(db.Integer)  # 阀门系列
    cad_status = db.Column(db.String(128))  # 模型状态
    press_class = db.Column(db.Integer)  # 压力等级
    temp_class = db.Column(db.Integer)  # 温度等级
    design_press = db.Column(db.FLOAT)  # 设计压力
    design_temp = db.Column(db.FLOAT)  # 设计温度
    shape_id = db.Column(db.String(32))  # 型线代号
    casing_mat_name = db.Column(db.String(128))  # 气缸材料
    stem_mat_name = db.Column(db.String(128))  # 提升杆材料
    fluid_medium_name = db.Column(db.String(128))  # 介质
    gov_mode = db.Column(db.String(128))  # 配汽方式
    install_mode = db.Column(db.String(128))  # 安装固定方式
    act_oil_press_mode = db.Column(db.String(128))  # 执行机构油压类型
    pilot_speedup = db.Column(db.BOOLEAN)  # 预启阀冲转
    act_conn_type = db.Column(db.String(128))  # 执行机构连接方式
    cost_level = db.Column(db.String(32))  # 成本
    total_weight = db.Column(db.FLOAT)  # 阀门总重
    industry = db.Column(db.BOOLEAN)  # 行业（工业透平适用）
    dwg_id = db.Column(db.String(128))  # 阀门图号
    turbine_unit_ids = db.Column(ARRAY(db.String(64)))  # 机组编号(制造单号)
    description = db.Column(db.String(128))  # 特性简介
    comments = db.Column(db.String(128))  # 备注
    used = db.Column(db.BOOLEAN)  # 是否选型

class ValveProducts(Base, ProductMixin):
    __tablename__ = 'valve_product_table'
    stop_throat_diam = db.Column(db.FLOAT)  # 主门口径/主阀喉部直径
    gov_throat_diam = db.Column(db.FLOAT)  # 调阀喉部直径
    ovld_throat_diam = db.Column(db.FLOAT)  # 补汽阀喉部直径
    stop_stem_lift = db.Column(db.FLOAT)  # 主阀阀杆行程
    stop_stem_lift_main = db.Column(db.FLOAT)  # 大阀行程
    stop_stem_lift_eql = db.Column(db.FLOAT)  # 预启阀行程
    gov_stem_lift = db.Column(db.FLOAT)  # 调阀阀杆行程
    ovld_stem_lift = db.Column(db.FLOAT)  # 补汽阀阀杆行程
    cv_calc = db.Column(db.FLOAT)  # Cv计算值
    cv = db.Column(db.FLOAT)  #
    feature_size_a = db.Column(db.FLOAT)  # 特征尺寸a
    feature_size_b = db.Column(db.FLOAT)  #
    feature_size_c = db.Column(db.FLOAT)  #
    feature_size_d = db.Column(db.FLOAT)  #
    feature_size_e_l = db.Column(db.FLOAT)  #
    out_conn_type = db.Column(db.String(128))  # 出口接口形式

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
    equiv_diam = db.Column(db.FLOAT)  # 当量口径
    gov_num = db.Column(db.Integer)  # 调门个数
    lever_num = db.Column(db.Integer)  # 杠杆个数
    gov_throat_diams = db.Column(ARRAY(db.FLOAT))  # 调阀喉部直径
    gov_stem_empty_lifts = db.Column(ARRAY(db.FLOAT))  # 调阀空行程
    gov_stem_max_lifts = db.Column(ARRAY(db.FLOAT))  # 调阀全开行程
    servo_max_lifts = db.Column(ARRAY(db.FLOAT))  # 油动机全开行程
    deleted = db.Column(db.Boolean, default=False)

    def delete(self):
        self.extra_info.delete()
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get(cls, id: Union[int, str]):
        pass


class Velocity(Base):

    __tablename__ = 'velocity_table'
    unit_run_mode = db.Column(db.String(128))
    press_loss_range = db.Column(ARRAY(db.FLOAT))
    velocity_range = db.Column(ARRAY(db.FLOAT))
    suitable_turbine_units = db.Column(db.String(128))
    comments = db.Column(db.String(128))

    def delete(self):

        db.session.delete(self)
        db.session.commit()

    @classmethod
    def name_infos(cls):
        return [
    {
        "cn_name": '机组运行方式',
        "name": 'unit_run_mode'
    },
    {
        "cn_name": '阀门总压损范围',
        "name": 'press_loss_range'
    },
    {
        "cn_name":"调阀喉部速度",
        "name": "velocity_range"
    },
    {
        "cn_name":"适用机组",
        "name": "suitable_turbine_units"
    },
    {
        "cn_name": "备注",
        "name": "comments"
    }
]

class ValveSeries(Base):
    id = db.Column(db.Integer, primary_key = True)
    code = db.Column(db.String(32))
    structure = db.Column(db.String(128))
    use_scene = db.Column(db.String(128))
    typical_turbine_units = db.Column(ARRAY(db.String(32)))
    sketch = db.Column(db.TEXT)

    @classmethod
    def name_infos(cls):
        return [
            {
                "cn_name": '阀门系列',
                "name": 'id'
            },
            {
                "cn_name": '代号',
                "name": 'code'
            },
            {
                "cn_name": '结构特点',
                "name": 'structure'
            },
            {
                "cn_name": "适用范围",
                "name": "use_scene"
            },
            {
                "cn_name": "典型机组",
                "name": "typical_turbine_units"
            },
            {
                "cn_name": "示意图",
                "name": "sketch"
            }
        ]


class Pressure(Base):
    design_press = db.Column(db.FLOAT)
    press_range = db.Column(ARRAY(db.FLOAT))
    update_by = db.Column(db.Integer)

    @classmethod
    def name_infos(cls):
        return [
            {
                "cn_name": '设计压力',
                "name": 'design_press'
            },
            {
                "cn_name": '压力等级',
                "name": 'press_range'
            }
        ]


class Temperature(Base):
    design_temp = db.Column(db.FLOAT)
    temp_range = db.Column(ARRAY(db.FLOAT))
    update_by = db.Column(db.Integer)

    @classmethod
    def name_infos(cls):
        return [
            {
                "cn_name": '设计温度',
                "name": 'design_temp'
            },
            {
                "cn_name": '温度等级',
                "name": 'temp_range'
            }
        ]


class ValveProductSchema(marshmallow.Schema):
    pass

class TemperatureSchema(marshmallow.Schema):
    # validate

    class Meta:
        fields = ('id', 'design_temp', 'temp_range')

class PressureSchema(marshmallow.Schema):
    # validate

    class Meta:
        fields = ('id', 'design_press', 'press_range')

class ValveSeriesSchema(marshmallow.Schema):
    # validate

    class Meta:
        fields = ('id', 'code', 'structure', 'use_scene', 'typical_turbine_units', 'sketch')

class VelocitySchema(marshmallow.Schema):
    # validate

    class Meta:
        fields = ('id', 'unit_run_mode', 'press_loss_range', 'velocity_range',
                  'suitable_turbine_units', 'comments')
