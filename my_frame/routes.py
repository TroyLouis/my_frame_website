from flask import render_template, url_for, flash, redirect, request, abort
from my_frame import app, db, bcrypt
from PIL import Image, ImageOps
from my_frame.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from my_frame.models import User, Image_Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os, uuid
from sqlalchemy import desc

def first_three_images_in_db():
    images = Image_Post.query.order_by(desc(Image_Post.id)).limit(3)
    image_dict = []
    for image in images:
        image_dict.append(image)
    return image_dict

@app.route("/")
@app.route("/home")
def home():
    images = first_three_images_in_db()
    return render_template('home.html', title='MyFrame', image=images)

@app.route("/register", methods=['GET', 'POST'])
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='MyFrame - Register', form=form, legend='New Post')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email and password and try again!', 'danger')
    return render_template('login.html', title='MyFrame - Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    folder_path = 'static/images/profile_pictures/'
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, folder_path, picture_fn)
    form_picture.save(picture_path)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def save_img_256x256(image):
    file_name = 'static/images/user_uploads_sized/'
    stored_file_name = 'static/images/user_uploads/'
    stored_file_path = os.path.join(app.root_path, stored_file_name, image)
    new_file_path = os.path.join(app.root_path, file_name, image)
    output = (256,256)
    with Image.open(stored_file_path) as im:
        resized_img = im.resize((output))
        resized_img.save(new_file_path)
        width,height = im.size
        print(width,height)

def user_images_group():
    all_images = Image_Post.query.all()
    empty_images=[]
    for image in all_images:
       if image.author.username == current_user.username:
        empty_images.append(image)
    return empty_images

@app.route("/account", methods=["GET","POST"])
@login_required
def account():
    form = UpdateAccountForm()
    user_images = user_images_group()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_picture = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_picture = url_for('static', filename='images/profile_pictures/' + current_user.profile_picture)
    return render_template('account.html', title='MyFrame - Account', profile_picture=profile_picture, form=form, images=user_images)

def save_user_upload(user_upload):
    uuid_hex = uuid.uuid4().hex
    folder_path = 'static/images/user_uploads/'
    _, f_ext = os.path.splitext(user_upload.filename)
    picture_fn = uuid_hex + f_ext
    picture_path = os.path.join(app.root_path, folder_path, picture_fn)
    user_upload.save(picture_path)
    return picture_fn

@app.route("/image/new", methods=["GET","POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_uuid = save_user_upload(form.picture.data)
            post = Image_Post(image=picture_uuid, title=form.title.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            save_img_256x256(picture_uuid)
            flash('Your image has been uploaded!', 'success')
            return redirect(url_for('account'))
        else:
            flash('Please select an image!', 'danger')
    return render_template('create.html', title='MyFrame - New Image', form=form)

@app.route("/edit/<int:id>", methods=["GET","POST"])
@login_required
def edit(id):
    image = Image_Post.query.get_or_404(id)
    if current_user.id != image.user_id:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        image.title = form.title.data
        db.session.commit()
        flash("Your image has been updated!", 'success')
        return redirect(url_for('edit', id=image.id))
    elif request == "GET":
        form.title.data = image.title
        form.picture.data = image.image
    return render_template('edit.html', title='MyFrame - Update Image', image=image,
                           form=form, legend='Update Post')

@app.route("/edit/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    image = Image_Post.query.get_or_404(id)
    if current_user.id != image.user_id:
        abort(403)
    db.session.delete(image)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('account'))

@app.route("/browse", methods=["GET","POST"])
@login_required
def browse():
    page = request.args.get('page', 1, type=int)
    images = Image_Post.query.paginate(page=page, per_page=1)
    return render_template('browse.html', title='MyFrame - Browse Images', image=images)


