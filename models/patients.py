import json

from boot import db, ma
from calculator.probability_counter import ProbabilityCounter
from models.gejala import Gejala
from models.penyakit import Penyakit
from models.rule_model import RuleModel


class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no_identitas = db.Column(db.String(100))
    nama = db.Column(db.String(50))
    alamat = db.Column(db.String(100))
    tgl_lahir = db.Column(db.Date)
    jenis_kelamin = db.Column(db.CHAR(1))
    history = db.Column(db.String(255))

    def __init__(self, *args):
        kwargs = args[0]
        self.nama = kwargs.get('nama', '')
        self.alamat = kwargs.get('alamat', '')
        self.tgl_lahir = kwargs.get('tgl_lahir', '')
        self.jenis_kelamin = kwargs.get('jenis_kelamin')
        self.history_patient = kwargs.get('history', '')

    @property
    def selected_model(self):
        model_id = self.history_patient.get('model')
        return RuleModel.query.get(model_id)

    @property
    def intensity_gejala(self):
        return self.history_patient.get('intensity')

    @property
    def possible_penyakit_sorted(self):
        counter = ProbabilityCounter(self.intensity_gejala, self.selected_model.model_)
        return counter.conclusions()

    @property
    def most_possible_penyakit(self):
        first_penyakit = self.possible_penyakit_sorted[0]
        first_penyakit_id = list(first_penyakit.keys())[0]
        return Penyakit.query.get(first_penyakit_id)

    @property
    def most_possible_penyakit_category(self):
        first_penyakit = self.possible_penyakit_sorted[0]
        return list(first_penyakit.values())[0][1]

    @property
    def named_intensity_gejala(self):
        gejala_query = Gejala.query
        intensity_gejala = self.intensity_gejala
        return [(gejala_query.get(x).nama, intensity_gejala.get(x)) for x in intensity_gejala.keys()]

    @property
    def named_intensity_gejala_formatted(self):
        return '. '.join(["%s dengan intensitas %s" % (x[0], x[1]) for x in self.named_intensity_gejala])

    @property
    def history_patient(self):
        return json.loads(self.history)

    @history_patient.setter
    def history_patient(self, value):
        self.history = json.dumps(value)

    @property
    def jk(self):
        if self.jenis_kelamin == 'l':
            return 'Laki-laki'
        elif self.jenis_kelamin == 'p':
            return 'Perempuan'
        else:
            return 'Tidak jelas'


class PatientSchema(ma.ModelSchema):
    class Meta:
        model = Patients
