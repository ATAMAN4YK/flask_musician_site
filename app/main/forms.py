from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from ..models import User, Albums
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    FileField, TextAreaField, DateField
from flask_login import current_user


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(),
        Length(1, 64)])

    password = PasswordField('Password', validators=[
        DataRequired()])

    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    username = StringField('Name', validators=[
        DataRequired(),
        Length(1, 64)])

    email = StringField('Email', validators=[
        DataRequired(),
        Length(1, 64)])

    password = PasswordField('Password', validators=[
        DataRequired()])

    repeat_password = PasswordField('Retype Password', validators=[
        DataRequired(),
        EqualTo('password', 'not equal')])

    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class AddNewAlbumForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(1, 64)])

    released = DateField('Released Date', validators=[
        DataRequired()
    ])

    genres = StringField('All genres', validators=[
        DataRequired(),
        Length(1, 128)
    ])

    description = StringField('Description', validators=[
        DataRequired(),
        Length(1, 128)])

    text = TextAreaField('Text', validators=[
        DataRequired(),
        Length(1, 2048)])

    language = StringField('Language', validators=[
        DataRequired(),
        Length(1, 32)
    ])

    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg'], 'Images only!')])

    submit = SubmitField('Сonfirm')

    def validate_name(self, field):
        if Albums.query.filter_by(name=field.data).first():
            raise ValidationError('Album name already in use.')


class EditAlbumForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(1, 64)])

    released = DateField('Released Date', validators=[
        DataRequired()
    ])

    genres = StringField('All genres', validators=[
        DataRequired(),
        Length(1, 128)
    ])

    description = StringField('Description', validators=[
        DataRequired(),
        Length(1, 128)])

    text = TextAreaField('Text', validators=[
        DataRequired(),
        Length(1, 2048)])

    language = StringField('Language', validators=[
        DataRequired(),
        Length(1, 32)
    ])

    submit = SubmitField('Сonfirm')

    def validate_name(self, field):
        album = Albums.query.filter_by(name=field.data).first()
        if album is not None and album.creator_id != current_user.id:
            raise ValidationError('Album name already in use.')
