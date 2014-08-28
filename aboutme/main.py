import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy 

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') \
    if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') else 'postgresql://postgres:postgres@localhost:5432/aboutmedb'
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
    def __init__(self, username = None, password = None, email = None, firstname = None, lastname = None,
        tagline = None, bio = None, avatar = None):
        self.username = username
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.tagline = tagline
        self.bio = bio
        self.avatar = avatar

@application.route('/')
@application.route('/<username>/')
def index(username=None):
    if not username:
        return render_template("index.html", page_title='Not implemented yet')

    user = Users.query.filter_by(username=username).first()
    if not user:
        user = Users()
        user.username = username
        user.firstname = 'Shaktimaan, is that you?'
        user.lastname = ''
        user.tagline = 'You are very special, you\'ll never be forgotten!'
        user.bio = 'Explain to the rest of the world, why you are the very most unique person to look at!'
        user.avatar = '/static/Shaktimaan.jpg'
        return render_template('aboutme.html', page_title = 'Claim this name: '+ username, user = user)

    return render_template('aboutme.html', page_title = user.firstname+' '+user.lastname, user = user)

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
                        avatar = '/static/avatar.jpg')
                    )
    db.session.commit()
    
if __name__ == '__main__':
    dbinit()
    application.run(debug=True, host="0.0.0.0", port=8888)