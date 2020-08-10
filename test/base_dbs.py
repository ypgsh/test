import unittest
import os
import sys
import json
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.main import create_app, db

from test.data import base_dbs_data

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
        # self._login()
        self._create_data()

    def _login(self):
        login_url = '/api/se_cloudcae/v1/login'
        resp = self.client.post(login_url, json=dict(
                                                        username="test_username",
                                                        password="test_password"
                                                    )
                                )
        assert resp.status_code == 200

    def _create_data(self):
        from app.models.base_data import Velocity, ValveSeries
        Velocity(**base_dbs_data.CREATE_VELOCITY_RECORD).save()

        ValveSeries(**base_dbs_data.CREATE_SERIES_RECORD).save()

    def test_basedbs(self):
        self._get_db_names()
        self._get_db_content()
        self._get_valve_series_brief()

    def _get_db_names(self):
        get_base_names_url = '/api/sec_valve/v1/base_dbs'
        resp = self.client.get(get_base_names_url)
        assert resp.status_code == 200



    def _get_db_content(self):
        db_name = 'velocity'
        args = ['unit_run_mode', 'press_loss_range', 'velocity_range',
                  'suitable_turbine_units', 'comments']
        get_db_content_url = f'/api/sec_valve/v1/base_dbs/{db_name}'
        resp = self.client.get(get_db_content_url, query_string=f'fields={json.dumps(args)}')
        assert resp.status_code == 200

    def _get_valve_series_brief(self):
        series_id = 1
        get_valve_series_brief_url = f'/api/sec_valve/v1/base_dbs/valve_series/{series_id}/brief'
        resp = self.client.get(get_valve_series_brief_url)
        assert resp.status_code == 200


if __name__ == '__main__':
    unittest.main()