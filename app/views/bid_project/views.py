from flask import Blueprint, request, g, current_app

from app.views.utils import json_response, jwt_authorize_required, ReturnCode

from .utils import BidProjectManager

bid_project = Blueprint('bid_project', __name__)


@bid_project.route('/bid_project', methods= ['POST'])
def create_project():
    args = request.get_json()
    return_code, data = BidProjectManager.create_project(**args)
    return json_response(201, code=return_code.value, data=data)


@bid_project.route('/bid_projects/<int:project_id>/data', methods= ['POST', 'GET'])
def project_data(project_id: int):
    if request.method == 'POST':
        args = request.get_json()
        return_code, data = BidProjectManager.modify_project_data(project_id, **args)
        return json_response(200, code=return_code.value)
    else:
        return_code, data = BidProjectManager.get_project_data(project_id)
        return json_response(200, code=return_code.value, data=data)


@bid_project.route('/bid_projects')
@bid_project.route('/bid_projects/<int:project_id>/brief')
def projects_brief_info(project_id: int = None):
    if not project_id:
        args = request.args
        return_code, data = BidProjectManager.get_projects(**args)
        return json_response(200, code=return_code.value, data=data)
    else:
        return_code, data = BidProjectManager.get_project_brief(project_id)
        return json_response(200, code=return_code.value, data=data)


@bid_project.route('/bid_project/<int:project_id>/matches')
def query_matches(project_id: int):
    return_code, data = BidProjectManager.get_matches(project_id)
    return json_response(200, code=return_code.value, data=data)

@bid_project.route('/bid_projects/<int:project_id>/form_data', methods= ['GET'])
def project_form_data(project_id: int):
    if request.method == 'GET':
        args = request.args
        if "form_id" not in args or not args.get('form_id'):
            return json_response(400, code=ReturnCode.FAILURE.value, message='form_id required')
        form_id =  args.get('form_id')
        return_code, data = BidProjectManager.get_form_data(project_id, form_id)
        return json_response(200, code=return_code.value, data=data)
    else:
        return json_response(405)