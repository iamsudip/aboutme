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

def dbinit(): 
    db.drop_all()
    db.create_all()
    db.session.add(Users(username='ekowibowo', firstname='Eko',
                        lastname='Suprapto Wibowo', password='rahasia',
                        email='swdev.bali@gmail.com',
                        tagline='A cool coder and an even cooler Capoeirista',
                        bio = 'I love Python very much!',
                        avatar = '/static/avatar.png')
                    )


@application.route('/')
@application.route('/<username>/')
def index(username=None):
    if not username:
        return render_template("aboutme.html", page_title="About me")
    return render_template("index.html", page_title='Not implemented yet')

if __name__ == '__main__':
    dbinit()
    application.run(debug=True, host="0.0.0.0", port=8888)