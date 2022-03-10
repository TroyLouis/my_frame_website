from flask_restful import Resource,reqparse, abort
from my_frame.models import Image_Post

image_ids = {}

def abort_if_nil_id(image_id):
    if image_id not in image_ids:
        abort(404, message='Item is unavailable.')

def abort_if_id_exists(image_id):
    if image_id in image_ids:
        abort(409, message="Already exists")


image_id_args = reqparse.RequestParser()
image_id_args.add_argument("image_post_id", type=int, help="Image Post ID is required.", required=True)

class FetchPost(Resource):
    def get(self, image_id):
        result = Image_Post.query.filter_by(id=image_id)
        for item in result:
            return item.image

    def put(self, image_id):
        abort_if_id_exists(image_id)
        args = image_id_args.parse_args()
        image_ids[image_id] = args
        return image_ids

    def delete(self,image_id):
        abort_if_nil_id(image_id)
        del image_ids[image_id]
        return "", 204



