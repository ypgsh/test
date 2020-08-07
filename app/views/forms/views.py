import json

from flask import Blueprint, request, g, current_app

from app.code import ReturnCode

from app.views.utils import json_response, jwt_authorize_required


from .utils import

form = Blueprint('form', __name__)


@form.route('/form', methods=['POST'])
def create_form():
    args = request.get_json()
    # TODO: validate
    name, input_args, code_content, desc = args.get('name'), args.get('input_args'), \
                                           args.get('code_content'), args.get('desc')
    return_code, msg = FunctionCodeManager().add_function(name, input_args, code_content, desc)
    if return_code is ReturnCode.SUCCESS:
        return json_response(201, code=ReturnCode.SUCCESS.value)
    else:
        return json_response(400, code = return_code.value, message = msg)
