from my_frame.models import Image_Post
from sqlalchemy import desc

def first_three_images_in_db():
    images = Image_Post.query.order_by(desc(Image_Post.id)).limit(3)
    image_list = []
    for image in images:
        image_list.append(image)
    return image_list

'''def uuid_from_list(list):
    uuid_list = []
    for uuid in list:
        uuid_list.append(uuid.image_uuid)
    return uuid_list'''