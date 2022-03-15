import os, uuid
from PIL import Image
from flask import current_app

def save_img_256x256(image):
    file_name = 'static/images/user_uploads_sized/'
    stored_file_name = 'static/images/user_uploads/'
    stored_file_path = os.path.join(current_app.root_path, stored_file_name, image)
    new_file_path = os.path.join(current_app.root_path, file_name, image)
    output = (256,256)
    with Image.open(stored_file_path) as im:
        resized_img = im.resize((output))
        resized_img.save(new_file_path)
        width,height = im.size
        print(width,height)

def save_user_upload(user_upload):
    uuid_hex = uuid.uuid4().hex
    folder_path = 'static/images/user_uploads/'
    _, f_ext = os.path.splitext(user_upload.filename)
    picture_fn = uuid_hex + f_ext
    picture_path = os.path.join(current_app.root_path, folder_path, picture_fn)
    user_upload.save(picture_path)
    return picture_fn
