
import json
import re
from flask import Blueprint, request, g, current_app

from app.code import ReturnCode

from app.views.utils import json_response, jwt_authorize_required

from .utils import BaseDBManager

base_dbs = Blueprint('base_dbs', __name__)


@base_dbs.route('/base_dbs', methods=['GET'])
@base_dbs.route('/base_dbs/<string:db_name>', methods=['GET'])
def base_dbs_operate(db_name: str = None):
    if db_name is None:
        return_code, data = BaseDBManager.get_base_dbs()
        return json_response(200, code=return_code.SUCCESS.value, data=data)
    else:
        args = request.args
        kwargs = dict()
        for k, v in args.items():
            if isinstance(v, (str,)) and re.match("^\[(.*)\]$", v):
                kwargs[k] = json.loads(v)
        return_code, data = BaseDBManager.get_db_datas(db_name, **kwargs)
        return json_response(200, code=return_code.value, data = data)


@base_dbs.route('/base_dbs/valve_series/<int:series_id>/brief', methods=['GET'])
def valve_series(series_id: int):
    return_code, data = BaseDBManager.get_valve_series_breif(series_id)
    return json_response(200, code=return_code.value, data=data)
