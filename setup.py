from setuptools import setup

setup(
    name='aboutme',
    version='1.0',
    description='This is my own about.me application to show my resume',
    author='iamsudip',
    author_email='iamsudip@programmer.net',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=[
        'bcrypt',
        'dnspython',
        'Flask==0.10.1',
        'Flask-SQLAlchemy==1.0',
        'Flask-Login==0.2.7',
        'Flask-WTF==0.9.2'
    ],
)
