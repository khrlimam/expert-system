import json

from boot import db, ma


class RuleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    deskripsi = db.Column(db.String(255))
    model = db.Column(db.Text())
    publish = db.Column(db.Boolean, default=False)

    @property
    def model_(self):
        return json.loads(self.model)

    @model_.setter
    def model_(self, value):
        self.model = json.dumps(value)


class RuleModelSchema(ma.ModelSchema):
    class Meta:
        model = RuleModel


rule_model_schema_many = RuleModelSchema(many=True)
rule_model_schema = RuleModelSchema()
