from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required

from app import db, app
from decorators import authAdmin
from models.models import Album, Song

albums = Blueprint('albums', __name__, url_prefix="/admin/albums")

# Імпорт бібліотек для наступної роботи при завантаженні зображень з форми у папку проекту
import os
from werkzeug.utils import secure_filename

# Папка, куди будуть збережені світлини
UPLOAD_FOLDER = 'static/uploads'
# Всі можливі роширення
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Додаємо конфіг та секретний ключ для безпеки
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'aboba'


# Функція, яка перевіряє чи підходить по формату завантажене зображення
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# all albums on one page
@albums.route('/')
@authAdmin
def index():
    album = Album.query.order_by(Album.date.desc()).all()
    return render_template("admin/albums/index.html", album=album)


@albums.route('/create-album', methods=['POST', 'GET'])
@authAdmin
def create_album():
    # POST:
    if request.method == 'POST':
        try:
            # Перевірка на те, чи є у запиті файл
            if 'file' not in request.files:
                flash('Немає шляху до файлу')
                return redirect(request.url)
            file = request.files['file']

            if file.filename == '':
                flash('Файл не обрано')
                return redirect(request.url)

            # Якщо все ОК, то зберігаємо файл у папку uploads у нашому проекті
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # Записуємо в окремі змінні назву та рік альбому
                name = request.form['name']
                date = request.form['date']
                description = request.form['description']

                # Створюємо об'єкт альбому, та аналогічно з User, через ORM додаємо запис в базу,
                # де image - назва картинка, до якої ми будемо звертатись уже в HTML,
                # прописуючи шлях static/uploads/image
                a = Album(date=date, name=name, src=filename, description=description)
                db.session.add(a)
                db.session.commit()

                # Переходимо до сторінки з альбомами
                return redirect('/admin/albums')
        except:
            db.session.rollback()
    # GET:
    return render_template("admin/albums/create-album.html")
    # if request.method == "POST":
    #     name = request.form['name']
    #     description = request.form['description']
    #     photo = request.files['photo']
    #     album = Album(name=name, description=description, photo=photo)
    #     try:
    #         db.session.add(album)
    #         db.session.commit()
    #         return redirect('/admin/albums')
    #     except:
    #         return "Error"
    # else:
    #     return render_template("admin/albums/create-album.html")


@albums.route('/<int:id>')
@authAdmin
def details(id):
    album = Album.query.get(id)
    return render_template("admin/albums/details.html", album=album)


@albums.route('/<int:id>/del')
@authAdmin
def posts_del(id):
    album = Album.query.get_or_404(id)
    try:
        db.session.delete(album)
        db.session.commit()
        return redirect('/admin/albums')
    except:
        return "при видаленні альбому відбулась помилка"


@albums.route('/<int:id>/update', methods=['POST', 'GET'])
@authAdmin
def post_update(id):
    # Дістаємо з БД потрібний запис та утворюємо відповідний об'єкт
    album = Album.query.get(id)

    # POST:
    if request.method == 'POST':
        try:
            file = ''

            # Якщо файл завантажено то зчитуємо його
            if 'file' in request.files:
                file = request.files['file']

            # Записуємо в окремі змінні назву та рік альбому
            name = request.form['name']
            date = request.form['date']
            description = request.form['description']

            # Якщо картинка правильна за розширенням та вона є
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # Робимо оновлення запису РАЗОМ З КАРТИНКОЮ
                db.session.query(Album).filter(Album.id == id).update(
                    {Album.name: name, Album.date: date, Album.description: description, Album.photo: filename})

            # Робимо оновлення запису БЕЗ КАРТИНКИ, лишається поточна
            else:
                db.session.query(Album).filter(Album.id == id).update(
                    {Album.name: name, Album.description: description, Album.date: date})

            # Комітимо зміни
            db.session.commit()
            return redirect('/admin/albums')
        except:
            # Якщо якась помилка, то відкатуємо назад і відміняємо коміт
            db.session.rollback()

    # GET:
    return render_template("admin/albums/update.html", album=album)
    # album = Album.query.get(id)
    # if request.method == "POST":
    #     album.name = request.form['name']
    #     album.description = request.form['description']
    #     album.photo = request.files['photo']
    #
    #     try:
    #         db.session.commit()
    #         return redirect('/admin/albums')
    #     except:
    #         return "при зміні альбому відбулась помилка"
    # else:
    #     return render_template("admin/albums/update.html", album=album)
