from datetime import datetime
from .model import User
from .model import Book
from .model import Loaning
from .db import db


def _time_source():
    return datetime.utcnow()


def current_time():
    return _time_source()


def find_user_by_id(user_id):
    return (
        db.session.query(User)
        .filter(
            User.id == user_id
        )
    ).first()


def find_user_by_username(username):
    return (
        db.session.query(User)
        .filter(
            User.username == username
        )
    ).first()


def get_books_list():
    return (
        db.session.query(Book)
    ).all()


def make_books_list_response(books):
    return [
        {
            "id": book.id,
            "title": book.title
        }
        for book in books
    ]


def find_book_by_id(book_id):
    return (
        db.session.query(Book)
        .filter(
            Book.id == book_id
        )
        .order_by(Book.id.asc())
    ).first()


def loan_book(user, book):
    loaning = Loaning(
        timestamp=current_time()
    )
    loaning.user = user
    loaning.book = book
    db.session.add(loaning)
    db.session.commit()


def make_loanings_list_response(loanings):
    return [
        {
            "id": book_id,
            "title": book_title,
            "time": timestamp
        }
        for timestamp, book_id, book_title in loanings
    ]


def get_user_loaned_books(user, start, end):
    query = (
        db.session.query(db.func.max(Loaning.timestamp), Book.id, Book.title)
        .join(Book, Loaning.book_id == Book.id)
        .filter(
            Loaning.user_id == user.id,
            Loaning.timestamp.between(start, end)
        )
        .group_by(Loaning.book_id)
        .order_by(Loaning.timestamp.desc())
    )

    return query.all()
