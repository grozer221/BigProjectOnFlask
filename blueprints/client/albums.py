from flask import Blueprint, render_template
from  app import db
from models.models import Album, Role, Song

clientAlbums = Blueprint('clientAlbums', __name__, url_prefix="/albums")


@clientAlbums.route('/')
def index():
    albums = Album.query.order_by(Album.date.desc()).all()
    return render_template("client/albums/index.html", albums=albums, Role=Role)


@clientAlbums.route('/<int:id>')
def details(id):
    album = Album.query.get(id)
    songs = db.session.query(Song).filter(album.id == Song.album_id).all()
    return render_template("client/albums/details.html", album=album, Role=Role, song=songs)
