#!/usr/bin/env python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Configuration

application = Flask(__name__)
application.config.from_object(Configuration)
db = SQLAlchemy(application)

from views import *

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
    
