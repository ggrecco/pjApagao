from flask import render_template
from flask_mail import Message
from app import mail, app
from threading import Thread
from time import time
import jwt


# enviar e-mail
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


# enviar corpo do e-mail
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()


# redefinir senha
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[PJ-Apagão] Redefina sua senha',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

# enviar confirmar email
def send_confirm_email(user, email, password, expires_in=600):
    token = jwt.encode({'confirm_email': email, 'exp': time() + expires_in},
                       app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    
    send_email('[PJ-Apagão] Confirme seu e-mail',
               sender=app.config['ADMINS'][0],
               recipients=[email],
               text_body=render_template('email/confirm_email.txt',
                                         user=user, token=token),
               html_body=render_template('email/confirm_email.html',
                                         user=user, email=email, password=password, token=token))
