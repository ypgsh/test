import json

from flask import Blueprint, request, g, current_app

from app.code import ReturnCode

from app.views.utils import json_response, jwt_authorize_required


from .utils import FunctionUseManager, FunctionCodeManager

function = Blueprint('function', __name__)


@function.route('/function', methods=['POST'])
def create_function():
    args = request.get_json()
    # TODO: validate
    name, input_args, code_content, desc = args.get('name'), args.get('input_args'), \
                                           args.get('code_content'), args.get('desc')
    return_code, msg = FunctionCodeManager().add_function(name, input_args, code_content, desc)
    if return_code is ReturnCode.SUCCESS:
        return json_response(201, code=ReturnCode.SUCCESS.value)
    else:
        return json_response(400, code = return_code.value, message = msg)


@function.route('/functions/<string:fn>/test', methods=['POST'])
def test_function(fn: str):
    args = request.get_json()
    try:
        result = FunctionUseManager().function_calc(fn, **args)
    except Exception as e:
        return json_response(400, code=ReturnCode.TEST_ERROR.value, message = e.args)
    else:
        return json_response(200, code=ReturnCode.SUCCESS.value, data = result)


@function.route('/functions/<string:fn>', methods=['GET', 'PATCH', 'DELETE'])
@function.route('/functions', methods=['GET'])
def function_operate(fn: str = None):
    if request.method == 'GET':
        if fn is not None:
            result = FunctionCodeManager().get_function_info(fn)
        else:
            args = request.args
            result = FunctionCodeManager().get_function_list(**args)
        return json_response(200, code=ReturnCode.SUCCESS.value, data = result)
    elif request.method == 'PATCH':
        args = request.get_json()
        _ = FunctionCodeManager().modify_function(fn, **args)
        return json_response(200, code=ReturnCode.SUCCESS.value)
    elif request.method == 'DELETE':
        args = request.get_json()
        _ = FunctionCodeManager().delete_function(fn)
        return json_response(200, code=ReturnCode.SUCCESS.value)
    else:
        return json_response(405)
