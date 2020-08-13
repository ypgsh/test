import jwt
import uuid
from functools import wraps
from datetime import timedelta, datetime
import json
from typing import Callable
from enum import Enum

from flask import make_response
from flask import current_app, request, g

from app.code import ReturnCode



class Role(Enum):
    SUPER_ADMIN=1
    ADMIN=2
    USER=3


def encode_token(payload: dict) -> tuple:
    """
    generate jwt token
    """
    try:
        today = datetime.today()
        zero_tm = datetime(today.year, today.month, today.day, 0, 0, 0)
        payload.update({'exp': zero_tm + timedelta(days=1)})
        return ReturnCode.SUCCESS, jwt.encode(
                        payload,
                        current_app.config.get('JWT_SECRET_KEY'),
                        algorithm='HS256'
                    ).decode()
    except Exception as e:
        return ReturnCode.FAILURE, e.args


def decode_auth_token(auth_token: str) -> tuple:
    """
    验证Token
    :param auth_token:
    :return: string or dict
    """
    try:
        payload = jwt.decode(auth_token, current_app.config.get('JWT_SECRET_KEY'), algorithms=['HS256'])
        return ReturnCode.SUCCESS, payload
    except jwt.DecodeError:
        return ReturnCode.FAILURE, 'secret error!'
    except jwt.ExpiredSignatureError:
        return ReturnCode.FAILURE, 'Token expired!'
    except jwt.InvalidTokenError:
        return ReturnCode.FAILURE, 'invalid token!'

def refresh_token(token: str) -> tuple:
    """
    refresh token
    :param token:
    :return:
    """
    return_code, payload =decode_auth_token(token)
    if return_code is not ReturnCode.SUCCESS:
        return return_code, payload
    return_code, new_token = encode_token(payload)
    return return_code, new_token


def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('token')
        res, payload = decode_auth_token(token)
        if isinstance(payload, (str,)):
            return json_response(status_code=401, result=1, msg=payload)
        g.payload=payload
        g.userId = payload.get('userId')
        g.privileges = payload.get('privileges')
        g.deptId = payload.get('deptId')
        if not all([g.userid, g.privileges]):
            return json_response(status_code=401, result=1, msg='无效Token!')
        return func(*args, **kwargs)
    return wrapper


def jwt_authorize_required(authorizeDict=None) -> Callable:
    def func_wrapper(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # if current_app.config.get('TESTING'):
            #     add_mock_info()
            #     return func(*args, **kwargs)
            jwt_token_name = current_app.config.get('JWT_TOKEN_NAME')

            token = request.headers.get(jwt_token_name)
            if not token:
                token = request.cookies.get(jwt_token_name)
            return_code, payload = decode_auth_token(token)
            if return_code is not ReturnCode.SUCCESS:
                return json_response(status_code=401, code=ReturnCode.NOT_LOGIN.value, message=payload)
            g.user_id = payload.get('user_id')
            g.user_name = payload.get('user_name')
            g.role_ids = payload.get('role_ids')
            g.office_name = payload.get('office_name')

            if authorizeDict and request.method in authorizeDict:
                if authorizeDict.get(request.method).value not in g.role_ids:
                    return json_response(status_code=403,
                                         code=ReturnCode.FORBIDDEN.value,
                                         message='admin role required'
                                         )

            response = func(*args, **kwargs)

            if token and response and (not request.base_url.endswith('/logout')):
                return_code, new_token = refresh_token(token)
                if return_code is not ReturnCode.SUCCESS:
                    json_response(status_code=400, code=return_code.value, message='refresh token error')
                response.set_cookie(jwt_token_name, new_token)

            return response

        return wrapper
    return func_wrapper


def add_mock_info():
    g.is_admin = True
    g.user_id = "test_user_id"
    g.user_name = 'test_user_name'
    g.office_name = 'test_office_name'


def json_response(status_code:int = 200,
                  headers: dict = None,
                  cookies:dict = None,
                  ensure_ascii: bool = False,
                  **kwargs):
    """
    format response data
    :param status_code:
    :param headers:
    :param kwargs:
    :return:
    """
    if headers is None:
        headers = dict()
    if cookies is None:
        cookies = dict()
    response_data = dict(kwargs) if kwargs else dict()
    response_data.update(dict(api_standard='1.0'))
    response = make_response(
        json.dumps(
            response_data,
            ensure_ascii=ensure_ascii),
        status_code)
    response.headers['Content-Type'] = 'application/json'
    for key, value in headers.items():
        response.headers[key] = value
    for key, value in cookies.items():
        response.set_cookie(key, value)
    return response

def get_uuid():
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, str(uuid.uuid1())))
