from boot import db, ma


class Gejala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))

    @property
    def nama_(self):
        return self.nama.title()

    @nama_.setter
    def nama_(self, v):
        self.nama = v.title()

    @property
    def kode_gejala(self):
        return "KG-%s" % str(self.id).zfill(2)


class GejalaSchema(ma.ModelSchema):
    class Meta:
        model = Gejala


gejala_schema = GejalaSchema(many=True)
