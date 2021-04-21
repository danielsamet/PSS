import hashlib
import os
from datetime import datetime

from flask import current_app
from flask_user import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, BadHeader
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm.collections import attribute_mapped_collection, column_mapped_collection
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from app.main.models import PhonemeRecording


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

    phoneme_recording_objects = db.relationship("PhonemeRecording", back_populates="user")
    phoneme_recordings = db.relationship(
        "PhonemeRecording", collection_class=column_mapped_collection(PhonemeRecording.__table__.c.phoneme_id),
        viewonly=True
    )

    # phoneme_recordings_local = association_proxy(
    #     "phoneme_recording_objects", "local_address",
    #     creator=lambda rel_dir, name, phoneme_id: PhonemeRecording(rel_dir, name, phoneme_id)
    # )

    # phoneme_recordings_web = association_proxy("phoneme_recording_objects", "text",
    #                                            creator=lambda step, text: PhonemeRecording(text, step))

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

    @property
    def user_parent_dir(self):
        # Allows for large number of users by separating all user folders into 16 different parent folders
        return hashlib.md5(str(self.email_address).encode('utf-8')).hexdigest().lower()[0]

    @property
    def user_secure_dir(self):
        # Allows for large number of users by separating all user folders into 16 different parent folders
        return os.path.join(self.user_parent_dir, str(self.id))

    @property
    def relative_recording_dir(self):
        return os.path.join(self.user_secure_dir, "recordings")

    def ensure_dir_is_built(self):
        for directory in [current_app.config["USER_DIR"], self.user_parent_dir, self.user_secure_dir,
                          self.relative_recording_dir]:
            if not os.path.isdir(directory):
                os.mkdir(directory)

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
