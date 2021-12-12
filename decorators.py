from flask import render_template
from flask_login import current_user

from models.models import Role


def authAdmin(function):
    def authAdminWrapper(*args, **kwargs):
        try:
            print('admin decorator!!', current_user.role)
            if current_user.role == Role.admin:
                return function(*args, **kwargs)
            return render_template('/admin/error.html', errorCode=401)
        except:
            return render_template('/admin/error.html', errorCode=401)
    authAdminWrapper.__name__ = function.__name__
    return authAdminWrapper
