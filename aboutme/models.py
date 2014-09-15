from main import db
from collections import OrderedDict


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

    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result