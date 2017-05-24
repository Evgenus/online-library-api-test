from .model import User
from .db import db


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
