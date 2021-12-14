from flask import Blueprint, render_template

from models.models import Album, Role

clientAlbums = Blueprint('clientAlbums', __name__, url_prefix="/albums")


@clientAlbums.route('/')
def index():
    albums = Album.query.order_by(Album.date.desc()).all()
    return render_template("client/albums/index.html", albums=albums, Role=Role)


@clientAlbums.route('/<int:id>')
def details(id):
    album = Album.query.get(id)
    return render_template("client/albums/details.html", album=album, Role=Role)
