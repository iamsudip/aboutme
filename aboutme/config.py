import os

class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') \
        if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') else 'postgresql://postgres:postgres@localhost:5432/aboutmedb'
    CSRF_ENABLED = True
    SECRET_KEY = 'youneedtoputasecretkeyhere'