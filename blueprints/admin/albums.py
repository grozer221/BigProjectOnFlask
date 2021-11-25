from app import db
from flask import Blueprint, render_template, request, redirect

from models.models import Album

albums = Blueprint('albums', __name__, url_prefix="/admin/albums")


# @albums.route('/')
# def index():
#     return render_template('admin/albums/index.html')

# all albums on one page
@albums.route('/')
def index():
    album = Album.query.order_by(Album.date.desc()).all()
    return render_template("admin/albums/index.html", album=album)


@albums.route('/create-album', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        src = request.form['src']
        album = Album(name=name, description=description, src=src)
        try:
            db.session.add(album)
            db.session.commit()
            return redirect('/admin/albums')
        except:
            return "Error"
    else:
        return render_template("admin/albums/create-album.html")


@albums.route('/<int:id>')
def details(id):
    album = Album.query.get(id)
    return render_template("admin/albums/details.html", album=album)



@albums.route('/<int:id>/del')
def posts_del(id):
    album = Album.query.get_or_404(id)
    try:
        db.session.delete(album)
        db.session.commit()
        return redirect('/admin/albums')
    except:
        return "при видаленні альбому відбулась помилка"


@albums.route('/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    album = Album.query.get(id)
    if request.method == "POST":
        album.name = request.form['name']
        album.description = request.form['description']
        album.src = request.form['src']

        try:
            db.session.commit()
            return redirect('/admin/albums')
        except:
            return "при зміні альбому відбулась помилка"
    else:
        return render_template("admin/albums/update.html", album=album)

