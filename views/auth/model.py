import json

from flask import Blueprint, render_template, request, jsonify, abort, make_response, redirect, url_for, flash

from boot import db
from models.gejala import Gejala, gejala_schema
from models.penyakit import Penyakit, schema as penyakit_schema
from models.rule_model import RuleModel, rule_model_schema
from views.auth import auth_group, login_required

model = Blueprint('model', __name__, url_prefix=auth_group('model'))


@model.route('/')
@login_required
def index():
    models = RuleModel.query.all()
    return render_template('auth/model/index.html', models=models)


@model.route('design', methods=['GET', 'POST', 'PATCH'])
@login_required
def add():
    if request.method == 'GET':
        penyakit = penyakit_schema.dumps(Penyakit.query.all())
        gejala = gejala_schema.dumps(Gejala.query.all())
        param = request.args.get("id")
        model = None
        model_data = {'publish': False, 'id': -1}
        if param:
            model_data = RuleModel.query.get_or_404(param)
            model = rule_model_schema.dumps(model_data).data
        return render_template('auth/model/add.html', penyakit=penyakit.data, gejala=gejala.data, model=model,
                               data=model_data)
    rule_model = RuleModel.query.get(request.form.get('id'))
    tmp = rule_model
    if tmp is None:
        rule_model = RuleModel()
    rule_model.publish = bool(int(request.form.get('publish')))
    rule_model.nama = request.form.get('nama')
    rule_model.deskripsi = request.form.get('deskripsi')
    rule_model.model_ = json.loads(request.form.get('model'))
    try:
        if request.method == 'POST' and tmp is None:
            db.session.add(rule_model)
        db.session.commit()
        return jsonify(message='Model telah disimpan', result=json.loads(rule_model_schema.dumps(rule_model).data))
    except Exception as e:
        abort(make_response(jsonify(message='Ada kesalahan! %s' % e), 400))


@model.route('delete/<id>')
@login_required
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


@model.route('toggle-publish/<id>')
@login_required
def toggle_publish(id):
    data = RuleModel.query.get_or_404(id)
    pub = data.publish
    if pub:
        data.publish = 0
    else:
        data.publish = 1
    db.session.commit()
    return redirect(url_for('model.index'))
