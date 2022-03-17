import click
from flask.cli import with_appcontext

from my_frame import db
from my_frame.models import User, Image_Post

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()