from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from werkzeug.wsgi import peek_path_info

import config
from models.login import Login
from models.rule_model import RuleModel

base = Blueprint('base', __name__)


@base.route('/try')
def try_():
    return peek_path_info(request.environ)


@base.route('/')
def index():
    r = RuleModel.query.filter_by(publish=True).all()
    return render_template('index.html', models=r)


@base.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return process_login()
    return render_template('login.html')


@base.route('/help')
def help():
    return render_template('help.html')


def process_login(*args, **kwargs):
    username = request.form.get('username')
    password = request.form.get('password')

    user = Login.query.get_or_404(username)
    isAuth = user.check_user(password)
    if isAuth:
        session[config.SESSION_USER_ID] = username
        return redirect(url_for('auth.index'))
    else:
        abort(status=404)
