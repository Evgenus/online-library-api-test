from .db import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(130))

    def __repr__(self):
        return '<User %r>' % (self.login)


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Book %r>' % (self.title)


class Loaning(db.Model):
    __tablename__ = 'loanings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(
        db.DateTime, index=True, nullable=False
    )

    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False
    )
    user = db.relationship('User', foreign_keys=[user_id])

    book_id = db.Column(
        db.Integer, db.ForeignKey('books.id'), nullable=False
    )
    book = db.relationship('book', foreign_keys=[book_id])
