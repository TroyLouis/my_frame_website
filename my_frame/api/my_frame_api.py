from flask_restful import Resource,reqparse, abort
from my_frame.models import Image_Post, User
from flask import url_for, redirect

IMAGE_IDS={}
def abort_if_nil_id(image_id):
    if image_id not in IMAGE_IDS:
        abort(404, message='Item is unavailable.')

def abort_if_id_exists(image_id):
    if image_id in IMAGE_IDS:
        abort(409, message="Already exists")

def query_image(image_id):
    result = Image_Post.query.filter_by(id=image_id)
    for image in result:
        return image.image

def get_user_id(email):
    email_exists = []
    result = User.query.filter_by(email=email)
    for item in result:
        email_exists.append(item.id)
    if not email_exists:
        abort(404, message="Does not exist.")
    return email_exists

def get_active_image(id):
    user = User.query.filter_by(id=id)
    for item in user:
        if not item:
            abort(404, message="Does not exist.")
        else:
            return item.active_image

image_id_args = reqparse.RequestParser()
image_id_args.add_argument("image_post_id", type=int, help="Image Post ID is required.", required=True)

class FetchPost(Resource):
    def get(self, image_id):
        image = query_image(image_id)
        return

    '''
    def put(self, image_id):
        abort_if_id_exists(image_id)
        args = image_id_args.parse_args()
        image_ids[image_id] = args
        return image_ids
    '''
    '''
    def delete(self,image_id):
        abort_if_nil_id(image_id)
        del image_ids[image_id]
        return "", 204
    '''
class FetchSetImage(Resource):
    def get(self, email):
        user_id = get_user_id(email)[0]
        active_image = get_active_image(user_id)
        return redirect(url_for('static', filename='images/user_uploads/' + active_image))



