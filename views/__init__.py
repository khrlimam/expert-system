from flask import Blueprint, render_template, request, jsonify

from models.rule_model import RuleModel

base = Blueprint('base', __name__)


@base.route('/try')
def try_():
    return 'Mantap!'


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
    return 'Help'


def process_login(*args, **kwargs):
    return jsonify(login='Gagal', username=request.form.get('email'), password=request.form.get('password'))
