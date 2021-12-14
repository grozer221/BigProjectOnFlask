from flask import Blueprint, render_template

from models.models import Role

clientSite = Blueprint('clientSite', __name__, url_prefix="/")


@clientSite.route('/')
def index():
    return render_template("client/site/index.html", Role=Role)
