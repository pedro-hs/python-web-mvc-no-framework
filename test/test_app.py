""" app.py test """
import unittest

from app import App
from router import Router
from webtest import TestApp


class AppTest(unittest.TestCase):
    def test_not_found(self):
        app = App(Router())
        app = TestApp(app)
        response = app.get('/invalid', expect_errors=True)
        assert response.status == '404 NOT FOUND'

    def test_internal_server_error(self):
        app = App({})
        app = TestApp(app)
        response = app.get('/invalid', expect_errors=True)
        assert response.status == '500 INTERNAL SERVER ERROR'

    def test_success(self):
        router = Router()

        @router('/valid', 'GET')
        def mock():
            return {'body': 'hi'}

        app = App(router)
        app = TestApp(app)
        response = app.get('/valid')
        assert response.status == '200 OK'
