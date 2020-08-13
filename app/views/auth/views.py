
import json

from flask import Blueprint, request, g, current_app

from app.code import ReturnCode

from app.views.utils import json_response, jwt_authorize_required, Role

from .utils import UserManager

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    args = request.get_json()
    username, password, is_super_admin = args.get('username'), args.get('password'), args.get('is_super_admin', False)
    if not all([username, password]):
        return json_response(400, code=ReturnCode.FAILURE, message='username or password required')
    return_code, jwt_token = UserManager.login(username, password, is_super_admin)
    if return_code is not ReturnCode.SUCCESS:
        return json_response(400, code=return_code.value, message=jwt_token)
    jwt_token_name = current_app.config.get('JWT_TOKEN_NAME')
    return json_response(200, code=return_code.value, cookies={jwt_token_name: jwt_token})


@auth.route('/logout', methods=['POST'])
def logout():
    resp = json_response(200, code=ReturnCode.SUCCESS.value)
    jwt_token_name = current_app.config.get('JWT_TOKEN_NAME')
    resp.delete_cookie(jwt_token_name)
    return resp


@auth.route('/current_user_info')
@auth.route('/auth')
@jwt_authorize_required()
def verifyToken():
    user_info = dict(user_name=g.user_name,
                     office_name=g.office_name,
                     is_admin=Role.ADMIN.value in g.role_ids
                     )
    return json_response(200, code=ReturnCode.SUCCESS.value, data=user_info)



