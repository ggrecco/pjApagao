from app import app, db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5
from time import time
import jwt


# cria banco de dados com campos id, username, email, password e posts
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    tackles = db.relationship('Tackle', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # define um hash para senha do  usuário
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # confirma o hash da senha do  usuário
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    # reset para password
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    # verifica o token do password
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    # # confirm e-mail
    # def get_email_token(self, email, expires_in=600):
    #     return jwt.encode(
    #         {'cofirm_email': email, 'exp': time() + expires_in},
    #         app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    # vrifica o token do e-mail
    @staticmethod
    def verify_email_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['confirm_email']
        except:
            return
        return User.query.get(id)


# armazena os dados enviados pelo hardware
class Tackle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    frequency = db.Column(db.String(140))
    city = db.Column(db.String(150))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Tackle {}>'.format(self.body)


# carrega usuário pelo id
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
