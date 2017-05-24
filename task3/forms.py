from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms import StringField
from wtforms import PasswordField
from wtforms import DateTimeField
from wtforms.validators import DataRequired

from .logic import find_user_by_username
from .logic import find_book_by_id
from .logic import current_time


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])

    _user = None

    def get_user(self):
        return self._user

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        self._user = find_user_by_username(self.username.data)
        if self._user is None:
            self.username.errors.append('No such user')
            return False

        if self._user.password != self.password.data:
            self.password.errors.append('Invalid password')
            return False

        return True


class LoanForm(FlaskForm):
    book_id = IntegerField("Book ID", validators=[
        DataRequired(message='Book ID is required')
    ])

    _book = None

    def get_book(self):
        return self._book

    def validate(self):
        if not super(LoanForm, self).validate():
            return False

        self._book = find_book_by_id(self.book_id.data)
        if self._book is None:
            self.book_id.errors.append('No such book')
            return False

        return True


class LoaningsListForm(FlaskForm):
    start = DateTimeField("Period Start", validators=[
        DataRequired(message='Period Start is required')
        ],
        format='%Y-%m-%d %H:%M:%S.%f'
    )

    end = DateTimeField("Period End", validators=[
        DataRequired(message='Period End is required')
        ],
        format='%Y-%m-%d %H:%M:%S.%f'
    )

    def validate(self):
        if not super(LoaningsListForm, self).validate():
            return False

        if self.start.data > self.end.data:
            self.start.errors.append('Invalid period bounds')
            return False

        if self.end.data > current_time():
            self.end.errors.append('End of the period should not be in future')
            return False

        return True

    def get_start(self):
        return self.start.data

    def get_end(self):
        return self.end.data
