from flask import Blueprint

from models.patients import Patients, PatientSchema

patient_profile = Blueprint('patient_profile', __name__, url_prefix='/admin/patient-profile')

patient_schema = PatientSchema()


@patient_profile.route('/<id>')
def show(id):
    result = Patients.query.get(id)
    return patient_schema.jsonify(result)
