from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# página inicial
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='PJA')


# página de loguin e formulário
@app.route('/login', methods=['GET', 'POST'])
def login():
    # verifica se o usuáro está logado
    if current_user.is_authenticated:
        # retorna para index caso usuáro logado
        return redirect(url_for('index'))

    # renderiza formulario de LoginForm
    form = LoginForm()

    # verifica formulário após submit
    if form.validate_on_submit():
        # recebe e filtra o usário
        user = User.query.filter_by(username=form.username.data).first()
        # verifica senha e usuário
        if user is None or not user.check_password(form.password.data):
            flash('Usuário ou senha incorretos.')
            return redirect(url_for('login'))
        # marca usuário como logado para navegação
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


# logout de usuário
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# pagina de cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Parabéns, agora você é um usuário registrado!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# página do perfil de usuário
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Suas modificações foram salvas com sucesso!')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
