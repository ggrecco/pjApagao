import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'you-shall-not-pass'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['en', 'pt']
    MAIL_SERVER = 'mx1.hostinger.com.br' # 'smtp.gmail.com'
    MAIL_PORT = 587 # 465
    MAIL_USE_TLS = 1
    MAIL_USERNAME = 'teste@casahacker.com.br'  # 'pjapagao'
    MAIL_PASSWORD = '#######' # 'Projeto-apagao'
    ADMINS = ['teste@casahacker.com.br'] # ['pjapagao@gmail.com.br']
    # MAIL_ASCII_ATTACHMENTS = False
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = 1
    # MAIL_USERNAME = 'pjapagao'
    # MAIL_PASSWORD = 'Projeto-apagao'
    # ADMINS = ['pjapagao@gmail.com.br']
