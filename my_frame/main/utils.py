from my_frame.models import Image_Post
from sqlalchemy import desc

def first_three_images_in_db():
    """
    :return: list of UUID's of the most recent three images stored to s3
    """
    images = Image_Post.query.order_by(desc(Image_Post.id)).limit(3)
    image_list = []
    for image in images:
        image_list.append(image)
    return image_list