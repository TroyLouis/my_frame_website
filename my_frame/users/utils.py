from my_frame.models import Image_Post
from flask import url_for
from flask_mail import Message
from flask_login import current_user
from my_frame import mail

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

