import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'you-shall-not-pass'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'mx1.hostinger.com.br' # 'smtp.gmail.com' 
    MAIL_PORT = 587 # 465
    MAIL_USE_TLS = 1
    MAIL_USERNAME = 'teste@casahacker.com.br'  # 'pjapagao'
    MAIL_PASSWORD = 'fSt2S9W8yNEC' # 'Projeto-apagao'
    ADMINS = ['teste@casahacker.com.br'] # ['pjapagao@gmail.com.br']
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['your-email@example.com']