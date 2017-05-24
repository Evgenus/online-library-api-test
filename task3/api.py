from flask import Blueprint
from flask import jsonify
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user

from .forms import LoginForm
from .forms import LoanForm
from .forms import LoaningsListForm
from .logic import get_books_list
from .logic import make_books_list_response
from .logic import loan_book
from .logic import get_user_loaned_books


api_bp = Blueprint('api', __name__)


@api_bp.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate():
        user = form.get_user()
        login_user(user)
        return jsonify(success=True)
    return jsonify(errors=form.errors)


@api_bp.route("/logout", methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify(success=True)


@api_bp.route("/books", methods=['GET'])
@login_required
def all_books_list():
    books_list = get_books_list()
    return jsonify(
        success=True, books=make_books_list_response(books_list)
    )


@api_bp.route("/loan", methods=['POST'])
@login_required
def perform_loan_book():
    form = LoanForm()
    if form.validate():
        book = form.get_book()
        loan_book(current_user, book)
        return jsonify(success=True)
    return jsonify(errors=form.errors)


@api_bp.route("/loanings", methods=['POST'])
@login_required
def get_loaned_books():
    form = LoaningsListForm()
    if form.validate():
        start = form.get_start()
        end = form.get_end()
        loanings_list = get_user_loaned_books(current_user, start, end)
        return jsonify(
            success=True,
            loanings=loanings_list
        )
    return jsonify(errors=form.errors)
