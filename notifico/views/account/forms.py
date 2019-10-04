from flask_login import current_user
import flask_wtf as wtf
from wtforms import fields as wtf_fields
from wtforms import validators as wtf_validators

from notifico.models import User
from notifico.services import reset


class UserRegisterForm(wtf.FlaskForm):
    username = wtf_fields.TextField('Username', validators=[
        wtf_validators.DataRequired(),
        wtf_validators.Length(min=2, max=50),
        wtf_validators.Regexp('^[a-zA-Z0-9_]*$', message=(
            'Username must only contain a to z, 0 to 9, and underscores.'
        ))
    ], description=(
        'Your username is public and used as part of your project name.'
    ))
    email = wtf_fields.TextField('Email', validators=[
        wtf_validators.DataRequired(),
        wtf_validators.Email()
    ])
    password = wtf_fields.PasswordField('Password', validators=[
        wtf_validators.DataRequired(),
        wtf_validators.Length(5),
        wtf_validators.EqualTo('confirm', 'Passwords do not match.'),
    ])
    confirm = wtf_fields.PasswordField('Confirm Password')

    def validate_username(form, field):
        from notifico.views.account import _reserved

        username = field.data.strip().lower()
        if username in _reserved or User.username_exists(username):
            raise wtf_validators.ValidationError(
                'Sorry, but that username is taken.'
            )


class UserLoginForm(wtf.FlaskForm):
    username = wtf_fields.TextField('Username', validators=[
        wtf_validators.DataRequired()
    ])
    password = wtf_fields.PasswordField('Password', validators=[
        wtf_validators.DataRequired()
    ])

    def validate_password(form, field):
        if not User.login(form.username.data, field.data):
            raise wtf_validators.ValidationError(
                'Incorrect username and/or password.'
            )


class UserPasswordForm(wtf.FlaskForm):
    old = wtf_fields.PasswordField('Old Password', validators=[
        wtf_validators.DataRequired()
    ])
    password = wtf_fields.PasswordField('Password', validators=[
        wtf_validators.DataRequired(),
        wtf_validators.Length(5),
        wtf_validators.EqualTo('confirm', 'Passwords do not match.'),
    ])
    confirm = wtf_fields.PasswordField('Confirm Password')

    def validate_old(form, field):
        if not User.login(current_user.username, field.data):
            raise wtf_validators.ValidationError('Old Password is incorrect.')


class UserDeleteForm(wtf.FlaskForm):
    password = wtf_fields.PasswordField('Password', validators=[
        wtf_validators.DataRequired(),
        wtf_validators.Length(5),
        wtf_validators.EqualTo('confirm', 'Passwords do not match.'),
    ])
    confirm = wtf_fields.PasswordField('Confirm Password')

    def validate_password(form, field):
        if not User.login(current_user.username, field.data):
            raise wtf_validators.ValidationError('Password is incorrect.')


class UserForgotForm(wtf.FlaskForm):
    username = wtf_fields.TextField('Username', validators=[
        wtf_validators.DataRequired()
    ])

    def validate_username(form, field):
        user = User.by_username(field.data)
        if not user:
            raise wtf_validators.ValidationError('No such user exists.')

        if reset.count_tokens(user) >= 5:
            raise wtf_validators.ValidationError(
                'You may not reset your password more than 5 times'
                ' in one day.'
            )


class UserResetForm(wtf.FlaskForm):
    password = wtf_fields.PasswordField('New Password', validators=[
        wtf_validators.DataRequired(),
        wtf_validators.Length(5),
        wtf_validators.EqualTo('confirm', 'Passwords do not match.'),
    ])
    confirm = wtf_fields.PasswordField('Confirm Password')
