
from functional import seq

from app.models.base_data import (Velocity, Temperature, Pressure, ValveSeries,
                                  VelocitySchema, TemperatureSchema, PressureSchema, ValveSeriesSchema)

from app.views.utils import ReturnCode

DB_LIST = [
    {
        "cn_name": '流速表',
        "name": 'velocity'
    },
    {
        "cn_name": '阀门系列表',
        "name": 'valve_series'
    },
    {
        "cn_name": "压力表",
        "name": "pressure"
    },
    {
        "cn_name": "温度表",
        "name": "temperature"
    }
]

DB_MODEL_REFLECT ={
    'temperature': Temperature,
    'valve_series': ValveSeries,
    'velocity': Velocity,
    'pressure': Pressure
}

DB_SCHEMA_REFLECT = {
    'temperature': TemperatureSchema,
    'valve_series': ValveSeriesSchema,
    'velocity': VelocitySchema,
    'pressure': PressureSchema
}


class ValveDBProxy:
    pass



def get_db_modle(db_name):
    pass

class BaseDBManager:
    @staticmethod
    def get_base_dbs():
        return ReturnCode.SUCCESS, DB_LIST

    @staticmethod
    def get_db_datas(db_name, **kwargs):
        db_model = DB_MODEL_REFLECT.get(db_name)
        if not db_model:
            return ReturnCode.FAILURE, f'{db_name} not available'
        name_infos = db_model.name_infos()
        fileds = None
        if 'fields' in kwargs:
            fileds = kwargs.pop('fields')
        invalid_keys = set(kwargs.keys()).difference({o['name'] for o in name_infos})
        if invalid_keys:
            _ = [kwargs.pop(key) for key in invalid_keys]
        obj_datas = db_model.query.filter_by(**kwargs).all()


        if fileds:
            header = seq(name_infos)\
                      .filter(lambda o: o['name'] in fileds)\
                      .to_list()
            body = seq(obj_datas)\
                      .map(lambda o: dict((filed, getattr(o, filed)) for filed in fileds))\
                      .to_list()

        else:
            header = name_infos
            body = DB_SCHEMA_REFLECT[db_name]().dump(obj_datas, many=True)
        result = dict(header=header, body=body)
        return ReturnCode.SUCCESS, result

    @staticmethod
    def get_valve_series_breif(series_id: int):
        obj = ValveSeries.get(series_id)
        if not obj:
            return ReturnCode.SUCCESS, 'NOT EXIST'
        data = ValveSeriesSchema(exclude=('id', 'code')).dump(obj)
        return ReturnCode.SUCCESS, data


