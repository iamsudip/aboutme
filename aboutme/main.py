import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy 
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators, HiddenField, TextAreaField, BooleanField
from wtforms.validators import Required, EqualTo, Optional, Length, Email

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
    email = db.Column(db.String(100), unique=True)
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
    email = TextField('Email address', validators=[
            Required('Please provide a valid email address'),
            Length(min=6, message=(u'Email address too short')),
            Email(message=(u'That\'s not a valid email address.'))])
    password = PasswordField('Create a password', validators=[
            Required(), Length(min=6, message=(u'Please give a longer password'))])
    username = TextField('Choose your username', validators=[Required()])
    agree = BooleanField('I agree all your terms of services',
            validators=[Required(u'You must accept our terms of service')])

@application.route('/')
def index():
    return render_template("index.html", page_title='Conversed / Your online presence!')

@application.route('/<username>/')
def userpage(username=None):
    user = Users.query.filter_by(username=username).first()
    if not user:
        user = Users()
        user.username = username
        user.firstname = 'Shaktimaan, is that you?'
        user.lastname = ''
        user.tagline = 'You are very special, you\'ll never be forgotten!'
        user.bio = 'Explain the rest of the world, why you are the most unique person to look at!'
        user.avatar = '/static/Shaktimaan.jpg'
        return render_template('aboutme.html', page_title='Claim this name: '+ username, user=user)
    return render_template('aboutme.html', page_title=user.firstname+' '+user.lastname, user=user)

@application.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form = SignupForm(request.form)
        if form.validate():
            pass
        else:
            return render_template('signup.html', form = form, page_title = 'Signup to Conversed!')
    return render_template('signup.html', form = SignupForm(), page_title = 'Signup to Conversed!')

def dbinit(): 
    db.drop_all()
    db.create_all()
    # Populating with data manually
    db.session.add(Users(username='iamsudip', firstname='Sudip',
                        lastname='Maji', password='nahi_bataunga',
                        email='iamsudip@programmer.net',
                        tagline='A cool coder and an even cooler Pythonista',
                        bio = 'I am a Pythonista and an open source enthusiast. I love sharing softwares,\
                        source code, ideas everything so I love the world of "FOSS". \
                        I like to implement my knowledge and learn while working on an exciting opportunity \
                        on software design and development.',
                        avatar = '/static/iamsudip.jpg')
                    )
    db.session.commit()

if __name__ == '__main__':
    dbinit()
    application.run(debug=True, host="127.0.0.1", port=8888)
    
