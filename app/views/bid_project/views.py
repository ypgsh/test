from flask import Blueprint, request, g, current_app

from app.views.utils import json_response, jwt_authorize_required

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
        pass

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