from my_frame.models import Image_Post
from sqlalchemy import desc

def first_three_images_in_db():
    images = Image_Post.query.order_by(desc(Image_Post.id)).limit(3)
    image_dict = []
    for image in images:
        image_dict.append(image)
    return image_dict