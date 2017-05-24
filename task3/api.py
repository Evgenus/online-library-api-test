from flask import Blueprint
from flask import jsonify
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

from .forms import LoginForm

api_bp = Blueprint('api', __name__)


@api_bp.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate():
        user = form.get_user()
        login_user(user)
        return jsonify(success=True)
    return jsonify(errors=form.errors)


@api_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify(success=True)
