from flask import Blueprint, render_template

albums = Blueprint('albums', __name__, url_prefix="/admin/albums")


@albums.route('/')
def index():
    return render_template('admin/albums/index.html')
