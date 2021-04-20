from datetime import datetime

from flask import current_app
from flask_user import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, BadHeader
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    created_at = db.Column(db.DateTime())
    confirmed = db.Column(db.Boolean(), default=False)
    void = db.Column(db.Boolean(), default=False)

    email_address = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(255), nullable=True, server_default='')
    last_seen = db.Column(db.DateTime())

    roles = db.relationship('Role', secondary='user_roles', back_populates="users")

    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password

        self.created_at = datetime.now().replace(microsecond=0)

        current_app.logger.info(f"New User {self} created")

    @property
    def password(self):
        # raise AttributeError("password is not a readable attribute")  # this would have been ideal but breaks
        # flask-user thus the following has been implemented instead
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=86400):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        current_app.logger.debug(f"{self} has generated a confirmation token")

        return s.dumps({"confirm": self.id}).decode('utf-8')

    def confirm_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token.encode('utf-8'))
        except (BadSignature, BadHeader):
            return False

        if data.get('confirm') != self.id:
            return False

        current_app.logger.debug(f"{self} has successfully confirmed a token")

        return True

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def email_confirmed_at(self):  # fake property for Flask-User
        return True

    def __repr__(self):
        return f'<User {self.email_address}>'


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    users = db.relationship('User', secondary='user_roles', back_populates="roles")

    def __init__(self, name):
        self.name = name
        current_app.logger.info(f"New Role {self} created")

    def __repr__(self):
        return f'<Role {self.name}>'


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


@login.user_loader
def get_user(ident):
    return User.query.get(int(ident))
