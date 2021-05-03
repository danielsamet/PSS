import requests
from flask import redirect, url_for, request, current_app, flash, jsonify
from flask_login import login_user, logout_user
from flask_user import current_user, login_required
from werkzeug.urls import url_parse

from app import db
from app.auth import auth
from app.auth.forms import LoginForm
from app.auth.models import User


def validate_recaptcha(recaptcha_response):
    verification_response = requests.get("https://www.google.com/recaptcha/api/siteverify", {
        "secret": current_app.config.get("RECAPTCHA_PRIVATE_KEY"),
        "response": recaptcha_response,
    })

    if verification_response.status_code == 200:
        return verification_response.json()["success"]

    return False


@auth.route("/login", methods=["POST"])
def login():
    """logs user in using email address"""

    if current_user.is_authenticated:
        return redirect(url_for('app.index'))

    form = LoginForm()
    if form.validate_on_submit():
        if not validate_recaptcha(request.form.get("recaptcha", "", str)):
            return jsonify({"msg": "Invalid reCaptcha details!"}), 400

        user = User.query.filter(db.func.lower(User.email_address) == form.email_address.data.lower()).first()
        password = form.password.data

        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            current_app.logger.debug(f'Failed login attempt for {form.email_address.data}')
            return jsonify({"msg": "Incorrect username or password"}), 400

        if user.void:
            flash('This account has been deleted. Please contact a system administrator if you believe this is a '
                  'mistake')
            current_app.logger.debug(f'Attempt to login to {user} denied as account is void')
            return jsonify({"msg": "Incorrect username or password"}), 400

        login_user(user, remember=form.remember_me.data)
        current_app.logger.debug(f'{user} has successfully logged in')
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '' or next_page == "/auth/logout":
            next_page = url_for('app.index')

        return redirect(next_page)

    return jsonify({"msg": "Hmm, something didn't seem to validate nicely there..."}), 400


@auth.route('/logout')
@login_required
def logout():
    """standard logout route"""

    user_id = current_user.id
    logout_user()
    current_app.logger.debug(f'{User.query.filter_by(id=user_id).first()} has logged out')

    return redirect(url_for('app.index'))


@auth.route('/register', methods=["POST"])
def register():
    """standard registration route"""
    form = LoginForm()
    if form.validate_on_submit():
        if not validate_recaptcha(request.form.get("recaptcha", "", str)):
            return jsonify({"msg": "Invalid reCaptcha details!"}), 400

        email_address = form.email_address.data

        if User.query.filter_by(email_address=email_address).first():
            return jsonify({"msg": "Email address already registered to an account!"}), 400

        user = User(email_address, form.password.data)
        db.session.add(user)
        db.session.commit()
        current_app.logger.debug(f'{user} has successfully registered!')

        login_user(user, remember=form.remember_me.data)
        current_app.logger.debug(f'{user} has successfully logged in!')

        return jsonify({"msg": "Success"}), 200

    return jsonify({"msg": "Registration failed!"}), 400
