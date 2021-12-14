from flask import render_template
from flask_login import current_user

from models.models import Role


def authAdmin(function):
    def authAdminWrapper(*args, **kwargs):
        try:
            print('admin decorator!!', current_user.role, current_user.role)
            if current_user.role == Role.admin:
                return function(*args, **kwargs)
            return render_template('/admin/error.html', errorCode=403)
        except:
            print('moderator decorator!! except')
            return render_template('/admin/error.html', errorCode=401)

    authAdminWrapper.__name__ = function.__name__
    return authAdminWrapper


def authModerator(function):
    def authModeratorWrapper(*args, **kwargs):
        try:
            print('moderator decorator!!', current_user.role, current_user.role)
            if current_user.role == Role.admin or current_user.role == Role:
                return function(*args, **kwargs)
            return render_template('/admin/error.html', errorCode=403)
        except:
            print('moderator decorator!! except')
            return render_template('/admin/error.html', errorCode=401)

    authModeratorWrapper.__name__ = function.__name__
    return authModeratorWrapper
