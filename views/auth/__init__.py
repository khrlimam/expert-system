def auth_group(url):
    return '/auth/%s' % url


from flask import Blueprint
from flask import render_template

auth = Blueprint('auth', __name__, url_prefix=auth_group(""))


@auth.route("/")
def index():
    return render_template('auth/base.html')
