#!/usr/bin/env python

import dns.resolver
import re
import wtforms

__all__ = ['ValidEmailDomain', 'ValidUserName']

class ValidEmailDomain(object):
    """
    Validator to confirm an email address is likely to be valid because its
    domain exists and has an MX record.

    :param str message: Optional validation error message. If supplied, this message overrides the following three
    :param str message_invalid: Message if the email address is invalid
    :param str message_domain: Message if domain is not found
    :param str message_email: Message if domain does not have an MX record
    """
    message_invalid = u"That is not a valid email address."
    message_domain = u"That domain does not exist."
    message_email = u"That email address does not exist."

    def __init__(self, message=None, message_invalid=None, message_domain=None, message_email=None):
        self.message = message
        if message_invalid:
            self.message_invalid = message_invalid
        if message_domain:
            self.message_domain = message_domain
        if message_email:
            self.message_email = message_email

    def __call__(self, form, field):
        email = re.match("^[a-zA-Z][\w\.-]*[a-zA-Z0-9]@[a-zA-Z][\w\.-]*[a-zA-Z0-9]\.[a-zA-Z][a-zA-Z\.]*[a-zA-Z]$", field.data.strip())
        if email:
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

class ValidUserName(object):
    """
    Validator to confirm an username is likely to be valid if it starts with an alphabet or digit and
    if it does not contains special character except underscore.

    :param str message: Optional validation error message. If supplied, this message overrides the following two
    :param str message_invalid: Message if the email address is invalid
    :param str message_starting_invalid: Message if username does not starts with alphanumeric character
    """
    message_invalid = u"That is not a valid username, use only alphanumeric characters and underscores."
    message_starting_invalid = u"Username should start with a number or character."

    def __init__(self, message=None, message_invalid=None, message_starting_invalid=None):
        self.message = message
        if message_invalid:
            self.message_invalid = message_invalid
        if message_starting_invalid:
            self.message_starting_invalid = message_starting_invalid

    def __call__(self, form, field):
        username = re.match("^[a-zA-Z0-9_]*$", field.data)
        if not username:
            raise wtforms.validators.StopValidation(self.message or self.message_invalid)
        if not field.data[0].isalnum():
            raise wtforms.validators.StopValidation(self.message or self.message_starting_invalid)

