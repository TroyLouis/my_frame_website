from flask import Blueprint
from flask_restful import Api

from my_frame.api.my_frame_api import FetchPost


# Initialize the API component.
api_blueprint = Blueprint("api", __name__)
_api = Api(api_blueprint)

# Register the resources of the API to it.
_api.add_resource(FetchPost, '/<string:image_id>')
