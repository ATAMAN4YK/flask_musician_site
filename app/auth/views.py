from flask import render_template, request, flash, redirect, url_for
from . import auth
from .. import db
from ..main.forms import LoginForm, RegistrationForm
from ..models import User
from flask_login import login_user, logout_user, login_required


@auth.route('/autorization', methods=['GET', 'POST'])
def autorization():
    form = LoginForm()

    if request.method == 'GET':
        return render_template('pages/autorization.html', form=form), 200

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None:
                if user.verify_password(form.password.data):
                    login_user(user, form.remember_me.data)
                    next = request.args.get('next')
                    if next is None or not next.startswith('/'):
                        next = url_for('main.home')
                    return redirect(next)
                else:
                    flash(message='Your password or login is not correct!',
                          category='warning')
                    return render_template('pages/autorization.html',
                                           form=form)
            else:
                flash(message='You do not registered in our site.',
                      category='info')
                return redirect(url_for('auth.registration'))
        else:
            flash(message='Your password or login is not correct!',
                  category='warning')
            return render_template('pages/autorization.html', form=form), 422


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash(message='You have been logged out.', category='info')
    return redirect(url_for('main.home'))


@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if request.method == 'GET':
        return render_template('pages/registration.html', form=form), 200

    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(email=form.email.data,
                            username=form.username.data,
                            password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash(message='You can now login.', category='info')
            return redirect(url_for('auth.autorization'))
        else:
            flash(message='Username is used or your password dont correct!',
                  category='warning')
            return render_template('pages/registration.html', form=form), 422
