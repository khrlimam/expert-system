import itertools

from flask import Blueprint, render_template, request, session, redirect, url_for

from boot import db
from calculator.probability_counter import ProbabilityCounter
from models.gejala import Gejala
from models.patients import Patients
from models.penyakit import Penyakit, schemas as penyakit_schema
from models.rule_model import RuleModel

consult = Blueprint('consult', __name__, url_prefix='/consult')


@consult.route('/')
def index():
    model = RuleModel.query.get_or_404(session['model-id'])
    listoflists = list(map(lambda x: x.get(list(x.keys())[0]), model.model_))
    gejala = [Gejala.query.get(x) for x in set(itertools.chain(*listoflists))]
    step = request.args.get('step')
    step_data = {}
    if step in session:
        step_data = session[step]
    gejala_s = []
    if 'gejala' in session:
        gejala_s = session['gejala']

    if step == 'intensitas':
        gejala = [Gejala.query.get(x) for x in gejala_s]

    result = {}

    if step == 'laporan':
        report_ = report()
        penyakit_query = Penyakit.query
        conclusions = report_.conclusions()
        probability = report_.probability()
        map_probability_to_array = [(list(x.keys())[0], list(x.values())[0]) for x in probability]
        highest_possibility_penyakit_id = list(conclusions[0].keys())[0]
        highest_possibility_penyakit_kategori = list(conclusions[0].values())[0][1]
        penyakit = penyakit_query.get(highest_possibility_penyakit_id)
        all_penyakit = penyakit_schema.dumps(Penyakit.query.all()).data
        profile = session['profile']
        intensitas_copy = session['intensitas'].copy()
        intensitas_copy.pop('step', None)
        gejala_user = [(Gejala.query.get(x).nama, intensitas_copy[x]) for x in intensitas_copy.keys()]
        result = {'penyakit': penyakit.nama,
                  'kategori': highest_possibility_penyakit_kategori,
                  'probability': probability,
                  'penyakits': all_penyakit,
                  'pr': map_probability_to_array,
                  'profile': profile,
                  'gejala_user': gejala_user}

    return render_template('guest/consult/consult.html', step=step, model=model, data=step_data, gejala=gejala,
                           gejala_s=gejala_s, result=result)


@consult.route('/for/<int:id>')
def for_(id):
    session['model-id'] = id
    return redirect('%s?step=profile' % url_for('consult.index'))


@consult.route('process', methods=['POST'])
def process():
    data = request.form
    step = data.get('step')
    session[step] = data
    if step == 'gejala':
        session[step] = list(map(int, request.form.getlist('gejala[]')))
    return redirect('%s?step=%s' % (url_for('consult.index'), steps.get(step)))


@consult.route('/done')
def done():
    data = session.get('profile')
    model_id = session.get('model-id')
    intensity_ = session.get('intensitas')
    intensity_.pop('step', None)
    data.update({'history': {'model': model_id, 'intensity': intensity_}})
    db.session.add(Patients(data))
    db.session.commit()
    for step in steps.keys():
        session.pop(step, None)
    session.pop('model-id', None)
    return redirect(url_for('base.index'))


def report():
    model_by_rule = RuleModel.query.get_or_404(session['model-id'])
    gejalas = session.get('gejala')
    session['intensitas'] = {x: 'mean' for x in gejalas}
    gejala_intensity = session.get('intensitas')
    selected_model = model_by_rule.model_
    return ProbabilityCounter(gejala_intensity, selected_model)


steps = {
    'profile': 'gejala',
    'gejala': 'laporan'
}
