import os


class Config(object):
    """
    Secret key that will be part of the request (cookies or variables).
    Minimal MongoDB settings
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or "secret_string"

    MONGODB_SETTINGS = {'db': 'UTA_Enrollment'}
    # OPTIONAL: 'host':'mongodb://localhost:27017/UTAEnrollment'
