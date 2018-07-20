from boot import db, ma


class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    no_identitas = db.Column(db.String(100))
    nama = db.Column(db.String(50))
    alamat = db.Column(db.String(100))
    tgl_lahir = db.Column(db.Date)
    jenis_kelamin = db.Column(db.CHAR(1))


class PatientSchema(ma.ModelSchema):
    class Meta:
        model = Patients
