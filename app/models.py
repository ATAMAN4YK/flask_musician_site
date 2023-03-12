from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager, db
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(64), unique=True, index=True, nullable=False)
    username = Column(String(64), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class Albums(UserMixin, db.Model):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    released = Column(Date, nullable=False)
    genres = Column(String(256), nullable=False)
    description = Column(String(256), nullable=False)
    text = Column(String(2048), nullable=False)
    language = Column(String(32), nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Album %r>' % self.name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
