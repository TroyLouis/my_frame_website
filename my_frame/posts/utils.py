import uuid
from my_frame.s3 import s3, s3_resource
from my_frame.config import Config


'''
#deprecated
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
'''

def fn_to_uuid(user_upload):
    """

    :param user_upload: User uploaded image's form.picture.data

    :return: User uploaded image's form.picture.data filename converted
        to a hex
    """
    uuid_hex = uuid.uuid4().hex
    user_upload.filename = uuid_hex
    return user_upload

''' 
#deprecated
def save_user_upload(user_upload):
    uuid_hex = uuid.uuid4().hex
    folder_path = 'static/images/user_uploads/'
    _, f_ext = os.path.splitext(user_upload.filename)
    picture_fn = uuid_hex + f_ext
    picture_path = os.path.join(current_app.root_path, folder_path, picture_fn)
    user_upload.save(picture_path)
    return picture_fn
'''

def upload_file_to_s3(file, bucket_name, acl="public-read"):
   """
   Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
   """
   try:
      s3.upload_fileobj(
         file,
         bucket_name,
         file.filename,
         ExtraArgs={
            "ACL": acl,
            "ContentType": file.content_type  # Set appropriate content type as per the file
         }
      )
   except Exception as e:
      print("Something Happened: ", e)
      return e
   return "{}{}".format(Config.S3_LOCATION, file.filename)

def del_file_from_s3(fn):
    """

    :param fn: uuid hex of image stored in database
    :return: object from amazon s3
    """
    s3.delete_object(Bucket='myframebucket', Key=fn)

def s3bucket_getfile(fn):
    obj = s3.get_object(Bucket=Config.S3_BUCKET, Key=fn)
    return obj
