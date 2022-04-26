from flask import Blueprint, render_template
from my_frame.main.utils import first_three_images_in_db
from my_frame.main.forms import NewsletterSignup
from flask import flash, request

main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET','POST'])
def home():
    images = first_three_images_in_db()
    form = NewsletterSignup()
    if request.method == "POST":
        if form.validate_on_submit():
            flash(f'Thank you for your interest, we will be adding a newsletter soon!', 'success')
        else:
            flash(f'Please enter a valid email address.', 'danger')
    return render_template('home.html', title='MyFrame', image=images, form=form)

@main.route("/setup")
def setup():
    return render_template('setup_guide.html', title='MyFrame - Setup')