#!/usr/bin/env python

import os

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy 
from flask.ext.wtf import Form
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from wtforms import TextField, PasswordField, HiddenField, TextAreaField, BooleanField
from wtforms.validators import Required, EqualTo, Optional, Length, Email

from utils import *

# Need to separte followings to config.py someday, this things making clumsy here
application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') \
    if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') else 'postgresql://postgres:postgres@localhost:5432/aboutmedb'
application.config['CSRF_ENABLED'] = True
application.config['SECRET_KEY'] = 'youneedtoputasecretkeyhere'
db = SQLAlchemy(application)

login_manager = LoginManager()
login_manager.init_app(application)
login_manager.login_view = '/signin'

@login_manager.user_loader
def load_user(id):
    """ Query authenticated users and return. """
    return Users.query.get(id)


# Need to separate models to models.py from main.py someday
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
    active = db.Column(db.Boolean)
    portfolio = db.relationship('Portfolio')
    
    def __init__(self, username=None, password=None, email=None, firstname=None, \
        lastname=None, tagline=None, bio=None, avatar=None, active=None):
        self.username = username
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.tagline = tagline
        self.bio = bio
        self.avatar = avatar
        self.active = active
    
    def is_authenticated(self):
        """ A method that'll always return True. """
        return True
    
    def is_active(self):
        """ 
        Returns user is active or not.
        Possible result is either True or False.
        """
        return self.active
    
    def is_anonymous(self):
        """
        This application doesn't support annonymous group and anonymous users both so
        always returns False.
        """
        return False
    
    def get_id(self):
        """ Returns unique id of an user. """
        return unicode(self.id)


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True)
    description = db.Column(db.Text)
    tags = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title=None, description=None, tags=None):
        self.title = title
        self.description = description
        self.tags = tags


# need to separate forms from main.py soon, looks seriously fucked up!
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


# it's a form too.
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



# need to separate views to views.py someday to manage things easily
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
        return render_template('aboutme.html', page_title='Claim this name: '+username, user=user, projectsform=ProjectsForm())
    return render_template('aboutme.html', page_title=user.firstname+' '+user.lastname, user=user, projectsform=ProjectsForm())

@application.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form = SignupForm(request.form)
        if form.validate():
            if form.password.data != form.repassword.data:
                form.repassword.errors.append(u'Passwords doesn\'t match.')
                return render_template('signup.html', signup_form=form, page_title='Signup to Conversed!')
            user = Users()
            user_exists = Users.query.filter_by(username=form.username.data).first()
            email_exists = Users.query.filter_by(email=form.email.data).first()
            if user_exists:
                form.username.errors.append(u'Username already taken')
            if email_exists:
                form.email.errors.append(u'Email already in use')
            if user_exists or email_exists:
                return render_template('signup.html', signup_form=form, page_title='Signup to Conversed!')
            else:
                # For testing purpose not created the form to take this data by users
                # need to fix
                # still populating data this way
                user.username = form.username.data
                user.email = form.email.data
                user.password = hashed_password(form.password.data.strip())
                user.firstname = u"foo"
                user.lastname = u"bar"
                user.tagline = u"foobar"
                user.bio = u"foobarfoobarfoobar foobarfoobar foobar foobar foobarfoobar foobarfoobarfoobar"
                user.avatar = '/static/favicon.png'
                db.session.add(user)
                db.session.commit()
                return render_template('signup_success.html', user=user, page_title='Registered to Conversed!')
        else:
            return render_template('signup.html', signup_form=form, page_title='Signup to Conversed!')
    return render_template('signup.html', signup_form=SignupForm(), page_title='Signup to Conversed!')

@application.route('/signin/', methods=['POST', 'GET'])
def signin():
    form = SigninForm(request.form)
    if request.method == 'POST':
        if current_user is not None and current_user.is_authenticated():
            return redirect(url_for('index'))
        if form.validate():
            user = Users.query.filter_by(username=form.username.data).first()
            if user is None:
                form.password.errors.append(u'Username or Password is wrong.')
                return render_template('signin.html', signin_form=form, page_title='Signin to Conversed!')
            # Make use of utils.safepass here
            if not validated_password(user.password, form.password.data):
                form.password.errors.append(u'Username or Password is wrong.')
                return render_template('signin.html', signin_form=form, page_title='Signin to Conversed!')
            login_user(user, remember=form.remember_me.data)
            session['signed'] = True
            session['username']= user.username
            if session.get('next'):
                next_page = session.get('next')
                session.pop('next')
                return redirect(next_page)
            else:
                return redirect(url_for("index"))
        else:
            return render_template('signin.html', signin_form=form, page_title='Signin to Conversed!')
    else:
        session['next'] = request.args.get('next')
        return render_template('signin.html', signin_form=SigninForm(), page_title='Signin to Conversed!')

# Not implemented yet
@application.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    return render_template('profile.html', page_title='Your online profile')

@application.route('/signout/', methods=['GET'])
def signout():
    try:
        session.pop('signed')
        username = session.pop('username')
        logout_user()
        return render_template('signout.html', page_title='Signned out succesfully!', username=username)
    except KeyError:
        return redirect(url_for('signin'))

# it should be in development.py cause it's only need to run when in development phase,
def dbinit():
    """
    Doc doc doc
    """ 
    db.drop_all()
    db.create_all()
    # Populating with data manually
    temp_user = Users(username=u'iamsudip',
        firstname=u'Sudip',
        lastname=u'Maji',
        password=hashed_password("nahi_bataunga"),
        email=u'iamsudip@programmer.net',
        tagline=u'A cool coder and an even cooler Pythonista',
        bio=u'I am a Pythonista and an open source enthusiast. I love sharing softwares,\
        source code, ideas everything so I love the world of "FOSS". \
        I like to implement my knowledge and learn while working on an exciting opportunity \
        on software design and development.',
        avatar=u'/static/iamsudip.jpg')
    temp_user.portfolio.append(Portfolio(title=u'pysub-dl',
        description=u'Commandline tool to download movie subtitles',
        tags=u'Python, BeautifulSoup, Requests'))
    temp_user.portfolio.append(Portfolio(title=u'DeCAPTCHas',
        description=u'Flipkart.com\'s captcha cracker', 
        tags=u'python, tesseract-ocr, PIL'))
    temp_user.portfolio.append(Portfolio(title=u'bdthankall',
        description=u'Thank all who wished you on your birthday in facebook',
        tags=u'python, fbconsole, facebook-graph-api'))
    temp_user.portfolio.append(Portfolio(title=u'sysmon',
        description=u'System process monitor CLI tool',
        tags=u'python, sqlite3'))
    db.session.add(temp_user)
    db.session.commit()

if __name__ == '__main__':
    dbinit()
    application.run(debug=True, host="127.0.0.1", port=8888)
    
