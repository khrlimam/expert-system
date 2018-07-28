import json

from flask import Blueprint, render_template, request, jsonify, abort, make_response, redirect, url_for, flash

from boot import db
from models.gejala import Gejala, gejala_schema
from models.penyakit import Penyakit, schema as penyakit_schema
from models.rule_model import RuleModel, rule_model_schema
from views.auth import auth_group

model = Blueprint('model', __name__, url_prefix=auth_group('model'))


@model.route('/')
def index():
    models = RuleModel.query.all()
    return render_template('auth/model/index.html', models=models)


@model.route('design', methods=['GET', 'POST', 'PATCH'])
def add():
    if request.method == 'GET':
        penyakit = penyakit_schema.dumps(Penyakit.query.all())
        gejala = gejala_schema.dumps(Gejala.query.all())
        param = request.args.get("id")
        model = None
        model_data = {'publish': False}
        if param:
            model_data = RuleModel.query.get_or_404(param)
            model = rule_model_schema.dumps(model_data).data
        return render_template('auth/model/add.html', penyakit=penyakit.data, gejala=gejala.data, model=model,
                               param=param, data=model_data)
    rule_model = RuleModel()
    if request.method == 'PATCH':
        rule_model = RuleModel.query.get(request.form.get('id'))
    rule_model.publish = bool(int(request.form.get('publish')))
    rule_model.nama = request.form.get('nama')
    rule_model.deskripsi = request.form.get('deskripsi')
    rule_model.model_ = json.loads(request.form.get('model'))
    try:
        if request.method == 'POST':
            db.session.add(rule_model)
        result = db.session.commit()
        return jsonify(message='Model telah disimpan', result=result)
    except Exception as e:
        abort(make_response(jsonify(message='Ada kesalahan! %s' % e), 400))


@model.route('delete/<id>')
def delete(id):
    data = RuleModel.query.get_or_404(id)
    name = data.nama
    try:
        db.session.delete(data)
        db.session.commit()
        flash("Data %s telah dihapus" % name)
        return redirect(url_for('model.index'))
    except Exception as e:
        abort(make_response(jsonify(message='Ada kesalahan! %s' % e), 400))
