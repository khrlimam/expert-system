from flask import Blueprint, render_template, request, jsonify

base = Blueprint('base', __name__)


@base.route('/')
def index():
    return render_template('index.html')


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
