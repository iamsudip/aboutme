#!/usr/bin/env python

#import dns.resolver
import os
import re

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 
from flask.ext.wtf import Form
import wtforms
from wtforms import TextField, PasswordField, validators, HiddenField, TextAreaField, BooleanField
from wtforms.validators import Required, EqualTo, Optional, Length, Email

from validators.validators import ValidEmailDomain

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') \
    if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') else 'postgresql://postgres:postgres@localhost:5432/aboutmedb'
application.config['CSRF_ENABLED'] = True
application.config['SECRET_KEY'] = 'youneedtoputasecretkeyhere'
db = SQLAlchemy(application)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    password = db.Column(db.String)
    email = db.Column(db.String(80), unique=True)
    time_registered = db.Column(db.DateTime)
    tagline = db.Column(db.String(255))
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(255))
    def __init__(self, username=None, password=None, email=None, firstname=None, \
        lastname=None, tagline=None, bio=None, avatar=None):
        self.username = username
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.tagline = tagline
        self.bio = bio
        self.avatar = avatar

class SignupForm(Form):
    email = TextField('Email address',
        validators=[Required(u"We need to confirm your email address to create the account"),
            Length(min=5, max=80, message=u"Address should be of length %(min)d to %(max)d characters"),
            Email(u"That does not appear to be a valid email address"),
            ValidEmailDomain()])
    password = PasswordField('Create a password',
        validators=[Required(), Length(min=6, message=(u'Please give a longer password minimum %(min)d characters'))])
    username = TextField(u'Choose your username', validators=[Required()])
    agree = BooleanField(u'I agree all your terms of services',
        validators=[Required(u'You must accept our terms of service')])

class ValidEmailDomain(object):
    """
    Validator to confirm an email address is likely to be valid because its
    domain exists and has an MX record.

    :param str message: Optional validation error message. If supplied, this message overrides the following three
    :param str message_invalid: Message if the email address is invalid
    :param str message_domain: Message if domain is not found
    :param str message_email: Message if domain does not have an MX record
    """
    message_invalid = u"That is not a valid email address"
    message_domain = u"That domain does not exist"
    message_email = u"That email address does not exist"

    def __init__(self, message=None, message_invalid=None, message_domain=None, message_email=None):
        self.message = message
        if message_invalid:
            self.message_invalid = message_invalid
        if message_domain:
            self.message_domain = message_domain
        if message_email:
            self.message_email = message_email

    def __call__(self, form, field):
        t = re.match("^[a-zA-Z][\w\.-]*[a-zA-Z0-9]@[a-zA-Z][\w\.-]*[a-zA-Z0-9]\.[a-zA-Z][a-zA-Z\.]*[a-zA-Z]$", field.data.strip())
        if t:
            email_domain = field.data.split('@')[-1]
            if not email_domain:
                raise wtforms.validators.StopValidation(self.message or self.message_invalid)
            try:
                dns.resolver.query(email_domain, 'MX')
            except dns.resolver.NXDOMAIN:
                raise wtforms.validators.StopValidation(self.message or self.message_domain)
            except dns.resolver.NoAnswer:
                raise wtforms.validators.StopValidation(self.message or self.message_email)
            except (dns.resolver.Timeout, dns.resolver.NoNameservers):
                pass
        else:
            raise wtforms.validators.StopValidation(self.message or self.message_invalid)

@application.route('/')
def index():
    return render_template("index.html", page_title='Conversed / Your online presence!')

@application.route('/<username>/')
def userpage(username=None):
    user = Users.query.filter_by(username=username).first()
    if not user:
        user = Users()
        user.username = username
        user.firstname = u'Shaktimaan, is that you?'
        user.lastname = u''
        user.tagline = u'You are very special, you\'ll never be forgotten!'
        user.bio = u'Explain the rest of the world, why you are the most unique person to look at!'
        user.avatar = u'/static/Shaktimaan.jpg'
        return render_template('aboutme.html', page_title='Claim this name: '+ username, user=user)
    return render_template('aboutme.html', page_title=user.firstname+' '+user.lastname, user=user)

@application.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form = SignupForm(request.form)
        if form.validate():
            user = Users()
            user_exist = Users.query.filter_by(username=form.username.data).first()
            email_exist = Users.query.filter_by(email=form.email.data).first()
            if user_exist:
                form.username.errors.append(u'Username already taken')
            if email_exist:
                form.email.errors.append(u'Email already in use')
            if user_exist or email_exist:
                return render_template('signup.html', form=form, page_title='Signup to Conversed!')
            else:
                # For testing purpose not created the form to take this data by users
                # need to fix
                # still populating data this way
                user.username = form.username.data
                user.email = form.email.data
                user.password = form.password.data
                user.firstname = u"foo"
                user.lastname = u"bar"
                user.tagline = u"foobar"
                user.bio = u"foobarfoobarfoobar foobarfoobar foobar foobar foobarfoobar foobarfoobarfoobar"
                user.avatar = '/static/favicon.png'
                db.session.add(user)
                db.session.commit()
                return render_template('signup_success.html', user=user, page_title='Registered to Conversed!')
        else:
            return render_template('signup.html', form=form, page_title='Signup to Conversed!')
    return render_template('signup.html', form=SignupForm(), page_title='Signup to Conversed!')

def dbinit(): 
    db.drop_all()
    db.create_all()
    # Populating with data manually
    db.session.add(Users(username=u'iamsudip',
        firstname=u'Sudip',
        lastname=u'Maji',
        password=u'nahi_bataunga',
        email=u'iamsudip@programmer.net',
        tagline=u'A cool coder and an even cooler Pythonista',
        bio=u'I am a Pythonista and an open source enthusiast. I love sharing softwares,\
        source code, ideas everything so I love the world of "FOSS". \
        I like to implement my knowledge and learn while working on an exciting opportunity \
        on software design and development.',
        avatar=u'/static/iamsudip.jpg')
    )
    db.session.commit()

if __name__ == '__main__':
    dbinit()
    application.run(debug=True, host="127.0.0.1", port=8888)
    
