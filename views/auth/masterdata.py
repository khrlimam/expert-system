from flask import Blueprint
from flask import render_template

from models.gejala import Gejala
from models.penyakit import Penyakit
from views.auth import auth_group, login_required

masterdata = Blueprint('master', __name__, url_prefix=auth_group('data'))


@masterdata.route('penyakit')
@login_required
def penyakit():
    models = Penyakit.query.all()
    return render_template('auth/penyakit/index.html', models=models)


@masterdata.route('gejala')
@login_required
def gejala():
    models = Gejala.query.all()
    return render_template('auth/gejala/index.html', models=models)
