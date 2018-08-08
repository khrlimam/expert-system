from boot import db, ma


class Penyakit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))

    @property
    def kode_penyakit(self):
        return "KP-%s" % str(self.id).zfill(2)

    @property
    def nama_(self):
        return self.nama.title()

    @nama_.setter
    def nama_(self, v):
        self.nama = v.title()


class PenyakitSchema(ma.ModelSchema):
    class Meta:
        model = Penyakit


schemas = PenyakitSchema(many=True)
schema = PenyakitSchema()
