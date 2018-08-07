from flask import Blueprint

from models.patients import Patients, PatientSchema
from views.auth import auth_group, login_required

patient = Blueprint('patient', __name__, url_prefix=auth_group('patient'))
patient_schema = PatientSchema()


@patient.route('/<id>')
@login_required
def show(id):
    result = Patients.query.get(id)
    return patient_schema.jsonify(result)
