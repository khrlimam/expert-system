from flask import Blueprint

from views.auth import auth_group

masterdata = Blueprint('master', __name__, url_prefix=auth_group('master'))


@masterdata.route('penyakit')
def penyakit():
    pass


@masterdata.route('gejala')
def gejala():
    pass
