from flask import Blueprint, render_template, request, redirect, flash, url_for
import os
from werkzeug.utils import secure_filename
from app import db, app
from models.models import Song, Album

songs = Blueprint('songs', __name__, url_prefix="/admin/songs")


UPLOAD_FOLDER_MUSIC = 'static/uploads/music'

ALLOWED_EXTENSION = {'mp3', 'ogg', 'wav'}

app.config['UPLOAD_FOLDER_MUSIC'] = UPLOAD_FOLDER_MUSIC
app.secret_key = 'adobe'


def allowed_format(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION


@songs.route('/')
def index():
    relationship = db.session.query(Album, Song).join(Song, Album.id == Song.album_id).all()
    return render_template('admin/songs/index.html', song=relationship)


@songs.route('/create', methods=['POST', 'GET'])
def add_song():
    if request.method == 'POST':
        try:
            if 'fileMusic' not in request.files:
                flash('Відсутній шлях до файлу')
                return redirect(request.url)

            file = request.files['fileMusic']
            if file.filename == '':
                flash('Ви не вибрали файл')
                return redirect(request.url)

            if file and allowed_format(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER_MUSIC'], filename))

            name_song = request.form['nameSong']
            selected_song = request.form['selectAlbum'];
            sn = Song(name=name_song, url=filename, album_id=selected_song)
            db.session.add(sn)
            db.session.commit()
            return redirect('/admin/songs')
        except:
            db.session.rollback()

    album = Album.query.all()
    return render_template('admin/songs/create.html', album=album)


@songs.route('/<int:id>')
def view(id):
    song = Song.query.get(id)
    return render_template("admin/albums/details.html", song=song)


@songs.route('/<int:id>/update', methods=['POST', 'GET'])
def update_song(id):
    song = Song.query.get(id)
    if request.method == 'POST':
        try:
            name_song = request.form['nameSong']
            db.session.query(Song).filter(Song.id == id).update({Song.name : name_song})
            db.session.commit()
            return redirect('/admin/songs')
        except:
            db.session.rollback()
    return render_template("admin/songs/update.html", song=song)


@songs.route('/<int:id>/delete')
def delete_song(id):
    song = Song.query.get_or_404(id)
    try:
        db.session.delete(song)
        db.session.commit()
        return redirect('/admin/songs')
    except:
        return "Error deleting song"