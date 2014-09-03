#!/usr/bin/env python

import bcrypt

__all__ = ['hashed_password', 'validated_password']

def hashed_password(password):
    """
    Returns password hash generated using bcrypt for the argument `password`.

    >>> hashed_password("secret")
    '$2a$12$sz9yYQ4IMjZDuzh2cexmfeWe77ncCgubA9Skiy0K1X8SJlRIVxPhS'

    >>> hashed_password(u"unicode_secret")
    '$2a$12$sz9yYQ4IMjZDuzh2cexsomerandomsubA9Skiy0K1X8SJlRIVxPhS'

    """

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def validated_password(password_hash, password):
    """
    Returns True if password and password_hash matches else False. 

    >>> validate_password('$2a$12$sz9yYQ4IMjZDuzh2cexmfeWe77ncCgubA9Skiy0K1X8SJlRIVxPhS', 'secret')
    True

    >>> validate_password('$2a$12$sz9yYQ4IMjZDuzh2cexmfeWe77ncCgubA9Skiy0K1X8SJlRIVxPhS', 'random')
    False

    >>> validate_password('$2a$12$sz9yYQ4IMjZDuzh2cexmfeWe77ncCgubA9Skiy0K1X8SJlRIVxPhS', u'secret')
    True

    """
    return bcrypt.hashpw(password.encode('utf-8'), password_hash.encode('utf-8')) == password_hash.encode('utf-8')