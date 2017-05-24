import unittest

from .app import create_app
from .db import db
from .model import User


class TestConfig:
    WTF_CSRF_ENABLED = False


class APITestCase(unittest.TestCase):

    def create_test_data(self):
        test_user = User(
            username="tester",
            password="tester"
        )
        db.session.add(test_user)
        db.session.commit()

    def setUp(self):
        self.app = create_app("test", config_obj=TestConfig)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.create_test_data()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_login(self):
        resp = self.client.post("/login", data={
            "username": "tester",
            "password": "tester"
        })

        self.assertEqual(resp.status_code, 200)

    def test_logout(self):
        resp = self.client.get("/logout")
        self.assertEqual(resp.status_code, 401)

        resp = self.client.post("/login", data={
            "username": "tester",
            "password": "tester"
        })

        self.assertEqual(resp.status_code, 200)

        resp = self.client.get("/logout")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.get("/logout")
        self.assertEqual(resp.status_code, 401)
