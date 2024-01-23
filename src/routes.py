from passlib.hash import sha256_crypt

from flask import render_template, render_template, request, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user

from . import __app, __db
from .forms import LoginForm, RegistrationForm, EditProfileForm
from .models import User

@__app.route('/')
def index():
    return render_template('index.html', users = User.query.all())

@__app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name = form.username.data).first()
        if user and sha256_crypt.verify(form.password.data, user.passwd):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
    return render_template('login.html', form = form)

@__app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Adding the user to the database
        hashed_password = sha256_crypt.hash(form.password.data)
        user = User(
            name = form.username.data,
            passwd = hashed_password
        )
        __db.session.add(user)
        __db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form = form)