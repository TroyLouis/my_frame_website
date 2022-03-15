from my_frame.models import Image_Post
from flask import url_for, current_app
import secrets, os
from flask_mail import Message
from PIL import Image
from flask_login import current_user
from my_frame import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    folder_path = 'static/images/profile_pictures/'
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, folder_path, picture_fn)
    form_picture.save(picture_path)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    msg.body=f'''To reset your password,visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.
    '''
    mail.send(msg)

def user_images_group():
    all_images = Image_Post.query.all()
    empty_images = []
    for image in all_images:
        if image.author.username == current_user.username:
            empty_images.append(image)
    return empty_images

