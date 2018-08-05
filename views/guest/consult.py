import itertools

from flask import Blueprint, render_template, request, session, redirect, url_for

from models.gejala import Gejala
from models.intensity import intensity, category
from models.penyakit import Penyakit, schema as penyakit_schema
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
        r = report()
        p = Penyakit.query
        report_ = r[0]
        prob = r[1]
        pr = [(list(x.keys())[0], list(x.values())[0]) for x in prob]
        penyakit_id = list(report_[0].keys())[0]
        kategori = list(report_[0].values())[0][1]
        penyakit = p.get(penyakit_id)
        all_penyakit = penyakit_schema.dumps(Penyakit.query.all()).data
        profile = session['profile']
        intensitas_copy = session['intensitas'].copy()
        intensitas_copy.pop('step')
        gejala_user = [(Gejala.query.get(x).nama, intensitas_copy[x]) for x in intensitas_copy.keys()]
        result = {'penyakit': penyakit.nama, 'kategori': kategori, 'probability': prob, 'penyakits': all_penyakit,
                  'pr': pr, 'profile': profile, 'gejala_user': gejala_user}

    return render_template('guest/consult/consult.html', step=step, model=model, data=step_data, gejala=gejala,
                           gejala_s=gejala_s, result=result)


@consult.route('/for/<int:id>')
def for_(id):
    session['model-id'] = id
    return redirect('%s?step=profile' % url_for('consult.index'))


@consult.route('process', methods=['POST'])
def process():
    step = request.form.get('step')
    session[step] = request.form
    if step == 'gejala':
        session[step] = list(map(int, request.form.getlist('gejala[]')))
    return redirect('%s?step=%s' % (url_for('consult.index'), steps.get(step)))


def report():
    r = RuleModel.query.get_or_404(session['model-id'])
    a = session['intensitas']
    a = {x: intensity.get(a.get(x), 0) for x in a.keys()}
    user_gejala = set(a.keys())
    thtmodel = r.model_
    user_penyakit = list(filter(lambda x: len(set(list(x.values())[0]).intersection(user_gejala)) > 0, thtmodel))
    user_penyakit_weighted = [{list(x.keys())[0]: [a.get(y, 0) for y in list(x.values())[0]]} for x in user_penyakit]
    prob = [{list(x.keys())[0]: sum(list(x.values())[0]) / len(list(x.values())[0])} for x in user_penyakit_weighted]
    sort_desc = sorted(prob, key=lambda item: -list(item.values())[0])
    conclusions = [{list(y.keys())[0]:
                        (list(y.values())[0],
                         list(filter(lambda x:
                                     isbetween(list(y.values())[0], x[1]),
                                     category))[0][0])} for y in sort_desc]
    return (conclusions, prob)


steps = {
    'profile': 'gejala',
    'gejala': 'intensitas',
    'intensitas': 'laporan'
}


def isbetween(x, tupple):
    return tupple[0] <= x <= tupple[1]
