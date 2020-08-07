import json

from flask import Blueprint, request, g, current_app

from app.code import ReturnCode

from app.views.utils import json_response, jwt_authorize_required


from .utils import FormManager, AttributeManager

form = Blueprint('form', __name__)


@form.route('/form', methods=['POST'])
def create_form():
    args = request.get_json()
    # TODO: validate

    return_code, data = FormManager.create_form(**args)
    if return_code is ReturnCode.SUCCESS:
        return json_response(201, code=ReturnCode.SUCCESS.value, data=data)
    else:
        return json_response(400, code = return_code.value, message = data)

@form.route('/forms', methods=['GET'])
def get_forms():
    args = request.args

    if {'module_name', 'page_name'}.difference(set(args.keys())):
        return json_response(400, code=ReturnCode.FAILURE.value, message='module_name and page_name required')
    return_code, data = FormManager.get_forms(**args)
    if return_code is ReturnCode.SUCCESS:
        return json_response(200, code=ReturnCode.SUCCESS.value, data=data)
    else:
        return json_response(400, code=return_code.value, message=data)



@form.route('/forms/<int:form_id>/attr', methods=['POST'])
@form.route('/forms/<int:form_id>/attrs', methods=['GET'])
@form.route('/forms/<int:form_id>/attrs/<int:form_attr_id>', methods=['GET'])
def form_attribute(form_id: int, form_attr_id: int = None):
    if request.method == 'POST':
        args = request.get_json()
        return_code, data = FormManager.add_attr(form_id=form_id, **args)
        if return_code is ReturnCode.SUCCESS:
            return json_response(201, code=ReturnCode.SUCCESS.value, data=data)
        else:
            return json_response(400, code=return_code.value, message=data)
    elif request.method == 'GET':
        assert form_id is not None
        if form_attr_id is None:
            return_code, data = FormManager.get_form_brief_attrs(form_id)
        else:
            return_code, data = FormManager.get_form_attr(form_attr_id)
        if return_code is ReturnCode.SUCCESS:
            return json_response(200, code=ReturnCode.SUCCESS.value, data=data)
        else:
            return json_response(400, code=return_code.value, message=data)



@form.route('/attr', methods = ['POST'])
def create_attr():
    args = request.get_json()
    # TODO: validate

    return_code, data = AttributeManager.create_attribute(**args)
    if return_code is ReturnCode.SUCCESS:
        return json_response(201, code=ReturnCode.SUCCESS.value, data=data)
    else:
        return json_response(400, code = return_code.value, message = data)


@form.route('/attrs', methods=['GET'])
@form.route('/attrs/<int:attr_id>', methods=['PATCH'])
def attr_operate(attr_id: int = None):
    if request.method == 'GET':
        args = request.args
         # TODO: validate

        return_code, data = AttributeManager.get_attributes(**args)
        if return_code is ReturnCode.SUCCESS:
            return json_response(200, code=ReturnCode.SUCCESS.value, data=data)
        else:
            return json_response(400, code=return_code.value, message=data)
    elif request.method == 'PATCH':
        args = request.get_json()
         # TODO: validate

        return_code, data = AttributeManager.modify_attr(attr_id=attr_id,**args)
        if return_code is ReturnCode.SUCCESS:
            return json_response(200, code=ReturnCode.SUCCESS.value, data=data)
        else:
            return json_response(400, code=return_code.value, message=data)
    else:
        return json_response(405)
