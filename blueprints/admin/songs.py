from flask import Blueprint, render_template

songs = Blueprint('songs', __name__, url_prefix="/admin/songs")


@songs.route('/')
def index():
    return render_template('admin/songs/index.html')
