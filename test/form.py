import unittest
import os
import sys
import json
import shutil
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.main import create_app, db

from test.data import form_data

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
        self._attr()
        self._form()
        self._form_render()
        # self._delete_function()

    def _attr(self):
        create_attr_url = '/api/sec_valve/v1/attr'
        resp = self.client.post(create_attr_url, json=form_data.CREATE_ATTR)
        assert resp.status_code == 201

        get_attrs_url = '/api/sec_valve/v1/attrs'
        resp = self.client.get(get_attrs_url)
        assert resp.status_code == 200

        attr_id = resp.json['data'][0].get('id')
        _ = form_data.CREATE_ATTR.pop('name')
        modify_attr_url = '/api/sec_valve/v1/attrs/{}'.format(attr_id)
        resp = self.client.patch(modify_attr_url, json=form_data.CREATE_ATTR)
        assert resp.status_code == 200

    def _form(self):
        create_form_url = '/api/sec_valve/v1/form'
        resp = self.client.post(create_form_url, json=form_data.CREATE_FORM)
        assert resp.status_code == 201
        form_id = resp.json['data']

        create_form_attr_url = '/api/sec_valve/v1/forms/{}/attr'.format(form_id)
        resp = self.client.post(create_form_attr_url, json=form_data.CREATE_FORM_ATTR)
        assert resp.status_code == 201

        get_page_forms_url = '/api/sec_valve/v1/forms'
        query_string = '&'.join([f'{key}={value}' for key, value in form_data.GET_PAGE_FORMS_ARGS.items()])
        resp = self.client.get(get_page_forms_url, query_string=query_string)
        assert resp.status_code == 200

        form_id = resp.json['data'][0]['id']

        get_form_attrs_url = '/api/sec_valve/v1/forms/{}/attrs'.format(form_id)
        resp = self.client.get(get_form_attrs_url)
        assert resp.status_code == 200
        form_attr_id = resp.json['data'][0]['id']

        get_form_attr_url = '/api/sec_valve/v1/forms/{}/attrs/{}'.format(form_id, form_attr_id)
        resp = self.client.get(get_form_attr_url)
        assert resp.status_code == 200

    def _form_render(self):
        get_page_forms_render_url = '/api/sec_valve/v1/form_render'
        query_string = '&'.join([f'{key}={value}' for key, value in form_data.GET_PAGE_FORMS_ARGS.items()])
        resp = self.client.get(get_page_forms_render_url, query_string=query_string)
        assert resp.status_code == 200


if __name__ == '__main__':
    unittest.main()
