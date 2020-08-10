from flask import Blueprint, request, g, current_app

from app.code import ReturnCode

from app.models.project import BidProject

from app.views.utils import json_response, jwt_authorize_required

from .utils import BidProjectManager

bid_project = Blueprint('bid_project', __name__)

@bid_project.route('/bid_project', methods= ['POST'])
def create_project():
    args = request.get_json()
    return_code, data = BidProjectManager.create_project(**args)
    return json_response(201, code=ReturnCode.value, data=data)