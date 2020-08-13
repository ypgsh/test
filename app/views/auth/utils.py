
from typing import Union
import requests

from flask import current_app

from mock_data import mock_user

from app.code import ReturnCode

from app.models.user import User, UserRole, Roles
from app.views.utils import Role, encode_token

class UserManager:

    @classmethod
    def get_id_by_name(cls, names: Union[str, list]) -> Union[str, list]:
        if current_app.config.get('TESTING') == True:
            if isinstance(names, (str, )):
                return mock_user.USER_ID
            else:
                return mock_user.USER_IDS

    @classmethod
    def get_name_by_id(cls, ids: Union[str, list]) -> Union[str, list]:
        if current_app.config.get('TESTING') == True:
            if isinstance(ids, (str, )):
                return mock_user.USER_NAME
            else:
                return mock_user.USER_NAMES

    @classmethod
    def _login_etech(cls, username: str, password: str) -> tuple:
        etech_auth_url = current_app.config.get('ETECH_AUTH_URL')
        client_id = current_app.config.get('ETECH_CLIENT_ID')
        client_secret = current_app.config.get('ETECH_CLIENT_SECRET')
        params = dict(
            grant_type="password",
            username=username,
            password=password,
            scope="OAUTH_DEMO",
            client_id=client_id,
            client_secret=client_secret
            )

        if current_app.config.get('TESTING') is True:
            return ReturnCode.SUCCESS, mock_user.ACCESS_TOKEN

        resp = requests.post(etech_auth_url, data=params)
        if resp.status_code == 200:
            data = resp.json().get('access_token')
            return_code = ReturnCode.SUCCESS
        else:
            data = resp.text
            return_code = ReturnCode.USERNAME_OR_PASSWORD_ERROR
        return return_code, data


    @classmethod
    def _get_etech_userinfo(cls, access_token: str)-> tuple:
        etech_user_info_url = current_app.config.get('ETECH_USER_INFO_URL')
        headers = {'Authorization': 'Bearer ' + access_token}

        if current_app.config.get('TESTING') is True:
            return ReturnCode.SUCCESS, dict(
                                            id=mock_user.ETECH_USER_INFO.get('code'),
                                            name=mock_user.ETECH_USER_INFO.get('name'),
                                            office_name=mock_user.ETECH_USER_INFO.get('detail').get('department')
                                        )

        resp = requests.get(etech_user_info_url, headers=headers)
        if resp.status_code == 200:
            data = resp.json().get('data')
            info = dict(
                id = data.get('code'),
                name = data.get('name'),
                office_name = data.get('detail').get('department')
            )
            return_code = ReturnCode.SUCCESS
        else:
            info = None
            return_code = ReturnCode.GET_USER_INFO_ERROR
        return return_code, info

    @classmethod
    def _create_user_record(cls, info: dict) -> tuple:
        user_obj = User.get(info['id'])
        if user_obj:
            return ReturnCode.SUCCESS, ''

        user_obj = User(**info).save()
        if not user_obj:
            return ReturnCode.FAILURE, 'error to save user info'
        user_role_obj = UserRole(
            user_id=user_obj.id,
            role_id=Role.USER.value
        ).save()
        if not user_role_obj:
            return ReturnCode.FAILURE, 'error to save role info'
        return ReturnCode.SUCCESS, ''

    @classmethod
    def _get_role_ids(cls, user_id: str) -> tuple:
        if current_app.config.get('TESTING') is True:
            return ReturnCode.SUCCESS, [Role.ADMIN.value]

        # TODO : one to many
        user_role_objs = UserRole.query.filter_by(user_id=user_id).all()
        return ReturnCode.SUCCESS, [o.role_id for o in user_role_objs]

    @classmethod
    def _check_super_admin(cls, username: str, password: str) -> ReturnCode:

        SUPER_ADMIN_NAME = current_app.config.get('SUPER_ADMIN_NAME')
        SUPER_ADMIN_PASSWORD = current_app.config.get('SUPER_ADMIN_PASSWORD')

        if username.strip() == SUPER_ADMIN_NAME and  password.strip() == SUPER_ADMIN_PASSWORD:
            return_code = ReturnCode.SUCCESS
        else:
            return_code = ReturnCode.USERNAME_OR_PASSWORD_ERROR
        return return_code

    @classmethod
    def login(cls, username: str, password: str, is_super_admin: bool = False) -> tuple:
        if is_super_admin is True:
            if cls._check_super_admin(username, password) is ReturnCode.SUCCESS:
                user_info = dict(
                    user_id=username,
                    user_name=username,
                    office_name='',
                    role_ids=[Role.SUPER_ADMIN.value]
                )
                return encode_token(user_info)
            else:
                return ReturnCode.USERNAME_OR_PASSWORD_ERROR, 'password error'

        return_code, access_token = cls._login_etech(username, password)
        if return_code is not ReturnCode.SUCCESS:
            return return_code, access_token

        return_code, user_info = cls._get_etech_userinfo(access_token)
        if return_code is not ReturnCode.SUCCESS:
            return return_code, access_token

        return_code, user_obj = cls._create_user_record(user_info)
        if return_code is not ReturnCode.SUCCESS:
            return return_code, user_obj
        _,  user_info['role_ids'] = cls._get_role_ids(user_info['id'])
        jwt_payload = dict(
                            user_id=user_info['id'],
                            user_name=user_info['name'],
                            role_ids = user_info['role_ids'],
                            office_name = user_info['office_name']
                            )
        return_code, jwt_token = encode_token(jwt_payload)
        return return_code, jwt_token




