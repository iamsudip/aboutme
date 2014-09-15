#!/usr/bin/env python

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, HiddenField, TextAreaField, BooleanField
from wtforms.validators import Required, EqualTo, Optional, Length, Email

from utils import ValidEmailDomain, ValidUserName


class SignupForm(Form):
    """
    Doc doc doc
    """
    email = TextField("Email address",
        validators=[Required(u"We need to confirm your email address to create the account."),
            Length(min=5, max=80, message=u"Address should be of length %(min)d to %(max)d characters."),
            Email(u"That does not appear to be a valid email address."),
            ValidEmailDomain()])
    username = TextField(u"Choose your username",
        validators=[Required(u"You forgot to enter username."),
            Length(min=3, message=(u"Minimum %(min)d characters.")),
            ValidUserName()])
    password = PasswordField("Create a password",
        validators=[Required(u"Please provide a password."),
            Length(min=6, message=(u"Please give a longer password minimum %(min)d characters"))])
    repassword = PasswordField("Re-type the password",
        validators=[Required(u"Please re-type the password."),
            Length(min=6, message=(u'Password doesn\'t match'))])
    agree = BooleanField(u'I agree all your terms of services',
        validators=[Required(u'You must accept our terms of service.')])


class SigninForm(Form):
    """
    Doc doc doc
    """
    username = TextField('Username', validators=[
        Required(u"You forgot to enter username."),
        Length(min=3, message=(u'Your username must be %(min)d characters.')),
        ValidUserName()
    ])
    password = PasswordField('Password', validators=[
        Required(u"Please provide a password."),
        Length(min=6, message=(u'Please give a longer password'))
    ])
    remember_me = BooleanField('Remember me', default=False)


class ProjectsForm(Form):
    """
    Doc doc doc
    """
    title = TextField('Title', validators=[
        Required("You must put the project name."),
        Length(min=3, message=(u'Title must be longer.'))
    ])
    description = TextField('Description', validators=[
        Required("You must put a project description."),
        Length(min=10, message=(u'A litle longer please'))
    ])
    tags = TextField('Tags', validators=[
        Length(min=3, message=(u'A litle longer please'))
    ])
