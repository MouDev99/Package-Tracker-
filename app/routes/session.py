from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_user
from sqlalchemy import or_
from app.forms.login_form import LoginForm
from app.forms.signup_form import SignupForm
from ..models import db, User

session_bp = Blueprint("session", __name__, url_prefix="/session")


@session_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(".index"))
    form = LoginForm()
    if form.validate_on_submit():
        print("submited the form")
        user_credential = form.credential.data
        user = User.query.filter(or_(User.user_name == user_credential,
                                 User.email == user_credential)).first()
        if not user or not user.check_password(form.password.data):
            form.login_error = "Incorrect (username/email) or/and passowrd"
            return render_template("login_form.html", form=form)

        login_user(user)
        return redirect("/")
    return render_template("login_form.html", form=form)


@session_bp.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user_data = {
            "user_name": form.data["user_name"],
            "email": form.data["email"]
        }
        user = User(**user_data)
        user.password = form.data["password"]

        db.session.add(user)
        db.session.commit()

        return redirect(url_for(".login"))

    return render_template("signup_form.html", form=form)
