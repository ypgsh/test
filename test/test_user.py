import unittest
import os
import sys
import json
import shutil
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.main import create_app, db

from test.data.task import test_data

app = create_app('test')


class ApiTest(unittest.TestCase):

    def setUp(self):
        print('starting')
        app.app_context().push()
        db.create_all()
        self.client = app.test_client()
        self.headers = None
        self.prepare_data()

    def tearDown(self):
        db.session.remove()  # must before db drop_all
        app.app_context().push()
        db.drop_all()
        print("ending")

    def prepare_data(self):
        pass
    def test_user(self):
        self._login()
        self._current_user_info()
        self._logout()

    def _login(self):
        login_url = '/api/se_cloudcae/v1/login'
        resp = self.client.post(login_url, json=dict(
                                                        username="test_username",
                                                        password="test_password"
                                                    )
                                )
        assert resp.status_code == 200

    def _current_user_info(self):
        get_current_user_url = '/api/se_cloudcae/v1/current_user_info'
        resp = self.client.get(get_current_user_url)
        assert resp.status_code == 200

    def _logout(self):
        logout_url = '/api/se_cloudcae/v1/logout'
        resp = self.client.post(logout_url)
        assert resp.status_code == 200

if __name__ == '__main__':
    unittest.main()
