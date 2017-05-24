from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired

from .logic import find_user_by_username

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
