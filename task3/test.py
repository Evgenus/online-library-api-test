import unittest
import json

from .app import create_app
from .db import db
from .model import User
from .model import Book


class TestConfig:
    WTF_CSRF_ENABLED = False


class APITestCase(unittest.TestCase):

    def create_test_data(self):
        test_user = User(
            username="tester",
            password="tester"
        )
        db.session.add(test_user)

        book_1 = Book(
            title="book1"
        )
        db.session.add(book_1)

        book_2 = Book(
            title="book2"
        )
        db.session.add(book_2)

        book_3 = Book(
            title="book3"
        )
        db.session.add(book_3)

        book_4 = Book(
            title="book4"
        )
        db.session.add(book_4)

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

    def test_books_list(self):
        resp = self.client.get("/books")
        self.assertEqual(resp.status_code, 401)

        resp = self.client.post("/login", data={
            "username": "tester",
            "password": "tester"
        })

        resp = self.client.get("/books")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data, {
          "books": [
            {
              "id": 1,
              "title": "book1"
            },
            {
              "id": 2,
              "title": "book2"
            },
            {
              "id": 3,
              "title": "book3"
            },
            {
              "id": 4,
              "title": "book4"
            }
          ],
          "success": True
        })
