from flask import Blueprint
from my_frame.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordForm, RequestResetForm
from flask import render_template, url_for, flash, redirect, request
from my_frame.models import User, Image_Post
from my_frame import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from my_frame.users.utils import user_images_group, save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data.lower(), email=form.email.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='MyFrame - Register', form=form, legend='New Post')

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check your email and password and try again!', 'danger')
    return render_template('login.html', title='MyFrame - Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=["GET","POST"])
@login_required
def account():
    form = UpdateAccountForm()
    user_images = user_images_group()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_picture = picture_file
        current_user.username = form.username.data.lower()
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_picture = url_for('static', filename='images/miscellanious/' + current_user.profile_picture)
    return render_template('account.html', title='MyFrame - Account', profile_picture=profile_picture, form=form, images=user_images)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    images = Image_Post.query.filter_by(author=user).order_by(Image_Post.date_posted.desc()).paginate(page=page, per_page=15)
    return render_template('browse_user.html', image=images, user=user)

@users.route("/reset_password", methods=["GET","POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password','info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='MyFrame - Reset Password', form=form)

@users.route("/reset_password/<token>", methods=["GET","POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token,', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been changed. You may now login.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='MyFrame - Reset Password', form=form)