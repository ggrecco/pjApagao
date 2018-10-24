from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, SendTackleFile, ResetPasswordRequestForm, ResetPasswordForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Tackle
from werkzeug.urls import url_parse
from datetime import datetime
from app.email import send_password_reset_email, send_confirm_email


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# página inicial(boas vindas)
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
# falta adicionar: confirmar o cadastro enviar o token para o banco de dados
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username=form.username.data
        email=form.email.data
        password=form.password.data
        send_confirm_email(username, email, password)
        flash('Verifique sua caixa de e-mails para confirmar seu cadastro')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# página do perfil de usuário
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


# página de edição do perfil de usuário
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
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


# página para teste de envio tackle
@app.route('/tackle', methods=['GET', 'POST'])
@login_required
def tackle():
    form = SendTackleFile()
    if form.validate_on_submit():
        flash('O cadastro realizado com suceso!')
        t = Tackle(frequency=form.frequency.data, city=form.city.data,
                    user_id=current_user.id)
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('tackle.html', title='Registrar Dados', form=form)



# solicita resete de senha(user informa email)
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('verifique a caixa de entrada do seu e-mail.')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Redefinir Senha', form=form)

        
# redefinição de senha
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Senha redefinida com sucesso.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


# confirmar e-mail
@app.route('/confirm_email/<user>/<email>/<password>/<token>', methods=['GET', 'POST'])
def confirm_email(user, email, password, token):            
    user = User(username=user, email=email, token_hash=token)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return render_template('confirm_email.html', user=user, email=email, password=password, token=token,title='Confirmação')
