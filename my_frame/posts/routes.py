from flask import Blueprint, render_template, url_for, redirect, flash, request, abort
from flask_login import current_user, login_required
from my_frame import db
from my_frame.models import Image_Post
from my_frame.posts.forms import PostForm, SetActiveForm
from my_frame.posts.utils import save_img_256x256, save_user_upload

posts = Blueprint('posts', __name__)


@posts.route("/image/new", methods=["GET","POST"])
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
            return redirect(url_for('users.account'))
        else:
            flash('Please select an image!', 'danger')
    return render_template('create.html', title='MyFrame - New Image', form=form, legend='Image Title')

@posts.route("/edit/<int:id>", methods=["GET","POST"])
@login_required
def edit(id):
    image = Image_Post.query.get_or_404(id)
    if current_user.id != image.user_id:
        abort(403)
    form = PostForm()
    image = Image_Post.query.get_or_404(id)
    form2 = SetActiveForm()
    single_image = image
    if form2.validate_on_submit():
        current_user.active_image = single_image.image
        db.session.commit()
        flash(f'Your active image has been changed to {single_image.title}', 'success')
    if form.validate_on_submit():
        image.title = form.title.data
        db.session.commit()
        flash("Your image has been updated!", 'success')
        return redirect(url_for('posts.edit', id=image.id))
    elif request == "GET":
        form.title.data = image.title
        form.picture.data = image.image
    return render_template('edit.html', title='MyFrame - Update Image', image=image,
                           form=form, form2=form2, legend='Update Post')

@posts.route("/edit/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    image = Image_Post.query.get_or_404(id)
    if current_user.id != image.user_id:
        abort(403)
    db.session.delete(image)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('users.account'))

@posts.route("/browse", methods=["GET","POST"])
#@login_required
def browse():
    page = request.args.get('page', 1, type=int)
    images = Image_Post.query.order_by(Image_Post.date_posted.desc()).paginate(page=page, per_page=12)
    return render_template('browse.html', title='MyFrame - Browse Images', image=images)


@posts.route("/posts/<int:id>", methods=["GET","POST"])
@login_required
def view_single_image(id):
    image = Image_Post.query.get_or_404(id)
    form = SetActiveForm()
    single_image = image
    if form.validate_on_submit():
        current_user.active_image = single_image.image
        db.session.commit()
        flash(f'Your active image has been changed to {single_image.title}', 'success')

    return render_template('view_single_image.html', form=form, title='MyFrame - Browse Images', image=single_image)