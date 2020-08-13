import unittest
import os
import sys
import json
import shutil
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.main import create_app, db

from test.data import functions_data

app = create_app('test')


class ApiTest(unittest.TestCase):

    def setUp(self):
        print('starting')
        app.app_context().push()
        db.create_all()
        self.client = app.test_client()
        self.headers = None
        # self.prepare_data()

    def tearDown(self):
        self._delete_function()
        db.session.remove()  # must before db drop_all
        app.app_context().push()
        db.drop_all()
        print("ending")

    def prepare_data(self):
        self._login()

    def _login(self):
        login_url = '/api/se_cloudcae/v1/login'
        resp = self.client.post(login_url, json=dict(
                                                        username="test_username",
                                                        password="test_password"
                                                    )
                                )
        assert resp.status_code == 200

    def test_functions(self):
        self._create_function()
        # self._delete_function()

    def _create_function(self):
        create_function_url = '/api/sec_valve/v1/function'
        resp = self.client.post(create_function_url, json=functions_data.CREATE_FUNCTION)
        assert resp.status_code == 201

        test_function_url = f'/api/sec_valve/v1/functions/{functions_data.CREATE_FUNCTION["name"]}/test'
        resp = self.client.post(test_function_url, json = functions_data.TEST_FUNCTION_ARGS)
        assert resp.status_code == 200
        assert resp.json['data'] == functions_data.TEST_FUNCTION_RESULT

    def _delete_function(self):
        delete_function_url = f'/api/sec_valve/v1/functions/{functions_data.CREATE_FUNCTION["name"]}'
        resp = self.client.delete(delete_function_url)
        assert resp.status_code == 200

if __name__ == '__main__':
    unittest.main()
