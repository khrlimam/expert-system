import json

from boot import db, ma


class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no_identitas = db.Column(db.String(100))
    nama = db.Column(db.String(50))
    alamat = db.Column(db.String(100))
    tgl_lahir = db.Column(db.Date)
    jenis_kelamin = db.Column(db.CHAR(1))
    history = db.Column(db.String(255))

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
