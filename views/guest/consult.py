import itertools

from flask import Blueprint, render_template, request, session, redirect, url_for

from models.gejala import Gejala
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
        result = report()

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
    got_gejala = session['gejala']
    model = RuleModel.query.get_or_404(session['model-id'])
    return session


steps = {
    'profile': 'gejala',
    'gejala': 'intensitas',
    'intensitas': 'laporan'
}
