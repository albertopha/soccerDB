import os

class Config(object):
    """
    Secret key that will be part of the request (cookies or variables).
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string"