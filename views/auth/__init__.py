import config
from models.login import Login
from models.patients import Patients
from views.auth.admin_only import login_required


def auth_group(url):
    return '/auth/%s' % url


from flask import Blueprint, redirect, url_for, g, session
from flask import render_template

auth = Blueprint('auth', __name__, url_prefix=auth_group(""))


@auth.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    username = session.get(config.SESSION_USER_ID)

    if username is None:
        g.user = None
    else:
        g.user = Login.query.get(username)


@auth.route("/")
@login_required
def index():
    patients = Patients.query.all()
    return render_template('auth/index.html', patients=patients)


@auth.route("/logout")
@login_required
def logout():
    session.pop(config.SESSION_USER_ID, None)
    return redirect(url_for('base.login'))
