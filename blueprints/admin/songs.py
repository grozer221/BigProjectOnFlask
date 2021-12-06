from flask import Blueprint, render_template, request, redirect, flash, url_for
import os
from werkzeug.utils import secure_filename
from app import db, app
from models.models import Song

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
    song = Song.query.order_by(Song.name).all()
    return render_template('admin/songs/index.html', song=song)


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

            sn = Song(name=name_song, url=filename)
            db.session.add(sn)
            db.session.commit()
            return redirect('/admin/songs')
        except:
            db.session.rollback()

    return render_template('admin/songs/create.html')


@songs.route('/<int:id>')
def view(id):
    song = Song.query.get(id)
    return render_template("admin/albums/details.html", song=song)
