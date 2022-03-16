from flask import Blueprint, render_template
from my_frame.main.utils import first_three_images_in_db

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    images = first_three_images_in_db()
    return render_template('home.html', title='MyFrame', image=images)


@main.route("/setup")
def setup():
    return render_template('setup_guide.html', title='MyFrame - Setup')