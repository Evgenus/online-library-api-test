import json
from datetime import datetime
from datetime import timedelta
import unittest
from unittest.mock import patch

from .app import create_app
from .db import db
from .model import User
from .model import Book
from .logic import find_user_by_username
from .logic import find_book_by_id
from .logic import loan_book


class TestConfig:
    WTF_CSRF_ENABLED = False


class APITestCase(unittest.TestCase):

    def create_test_data(self):
        test_user = User(
            username="tester",
            password="tester"
        )
        db.session.add(test_user)

        another_user = User(
            username="tester2",
            password="tester2"
        )
        db.session.add(another_user)

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

    def test_books_loaning(self):
        resp = self.client.post("/loan", data={
            "book_id": 1
        })
        self.assertEqual(resp.status_code, 401)

        resp = self.client.post("/login", data={
            "username": "tester",
            "password": "tester"
        })

        resp = self.client.post("/loan", data={
        })
        self.assertEqual(resp.status_code, 400)

        resp = self.client.post("/loan", data={
            "book_id": 5
        })
        self.assertEqual(resp.status_code, 400)

        resp = self.client.post("/loan", data={
            "book_id": 1
        })
        self.assertEqual(resp.status_code, 200)

    @patch("task3.logic._time_source")
    def test_loaning_list(self, time_mock):
        resp = self.client.post("/loanings", data={
            "start": 1
        })
        self.assertEqual(resp.status_code, 401)

        resp = self.client.post("/login", data={
            "username": "tester",
            "password": "tester"
        })

        now = datetime(2017, 5, 24, 9, 33, 13, 1)

        # a bit of time traveling :)
        time_mock.return_value = now - timedelta(days=10 * 30)
        resp = self.client.post("/loan", data={
            "book_id": 1
        })

        time_mock.return_value = now - timedelta(days=5 * 30)
        resp = self.client.post("/loan", data={
            "book_id": 2
        })

        # same book loaned twice by same user
        time_mock.return_value = now - timedelta(days=2 * 30)
        resp = self.client.post("/loan", data={
            "book_id": 2
        })

        # book loaned by another user
        time_mock.return_value = now - timedelta(days=1 * 30)
        with self.app.app_context():
            book_3 = find_book_by_id(3)
            another_user = find_user_by_username("tester2")
            loan_book(another_user, book_3)

        time_mock.return_value = now

        resp = self.client.post("/loanings", data={
            "start": now - timedelta(days=365),
            "end": now - timedelta(seconds=1)
        })
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.get_data(as_text=True))
        self.assertEqual(data, {
          "loanings": [
            {
              "id": 2,
              "time": "Sat, 25 Mar 2017 09:33:13 GMT",
              "title": "book2"
            },
            {
              "id": 1,
              "time": "Thu, 28 Jul 2016 09:33:13 GMT",
              "title": "book1"
            }
          ],
          "success": True
        })
