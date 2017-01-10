import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = 'DEBUG'
DEBUG = True

ADMINS = frozenset(['youremail@yourdomain.com'])
SECRET_KEY = 'KEY'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

WTF_CSRF_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = 'publicKey'
RECAPTCHA_PRIVATE_KEY = 'privateKey'
RECAPTCHA_OPTIONS = {'theme': 'white'}

