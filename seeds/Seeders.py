import json

from boot import db
from models.gejala import Gejala
from models.login import Login
from models.penyakit import Penyakit
from models.rule_model import RuleModel
from seeds.Seeder import Seeder

penyakits = [
    "abses parafaring",
    "faringitis akut",
    "Faringitis kronis",
    "laringitis akut",
    "laringitis kronis",
    "meniere",
    "otitis media eksterna",
    "otitis media akut (OMA)",
    "polip hidung",
    "Rinitis alergi",
    "Rinitis Hipertrofi",
    "Sinusitis",
    "Tonsilitis Akut",
    "Tonsilitis Kronis",
    "Vestibularis"
]

gejalas = [
    "Batuk",
    "Batuk dengan dahak kental",
    "Badan terasa lesu",
    "Bersin-bersin",
    "Dahak ditenggorokan",
    "Demam",
    "Gangguan penciuman",
    "Gangguan pengecapan",
    "Hidung keluar ingus",
    "Hidung tersumbat",
    "Leher kaku",
    "Mual dan muntah",
    "Mata dan tenggorokan gatal",
    "Nyeri kepala",
    "Nyeri pada muka",
    "Nyeri saat menelan",
    "Nyeri pangkal hidung",
    "Pembengkakan diliang telinga",
    "Pembengkakan kelenjar limfe",
    "Pendengaran berkurang",
    "Perasaan mengganjal ditenggorokan",
    "Nyeri tenggorokan",
    "Suara serak",
    "Suara sengau",
    "Mulut berbau",
    "Telinga nyeri",
    "Telinga gatal-gatal",
    "Telinga terasa ada cairan",
    "Terasa ada benjolan dihidung",
    "Telinga terasa penuh",
    "Tenggorokan kering",
    "Telinga terasa gatal",
    "Telinga tersumbat"
]


class PenyakitSeeder(Seeder):

    def run(self):
        for penyakit in penyakits:
            p = Penyakit()
            p.nama_ = penyakit
            db.session.add(p)
            db.session.commit()


class GejalaSeeder(Seeder):

    def run(self):
        for gejala in gejalas:
            g = Gejala()
            g.nama_ = gejala
            db.session.add(g)
            db.session.commit()


class DefaultUser(Seeder):
    def run(self):
        user = Login()
        user.username = 'admin'
        user.password_ = 'secret'
        db.session.add(user)
        db.session.commit()


class RuleModelSeeder(Seeder):
    def run(self):
        rule_model = RuleModel()
        rule_model.nama = 'THT'
        rule_model.deskripsi = 'Model THT untuk pasien THT'
        with open('rules.json', 'r') as f:
            r = json.loads(f.read())
            rule_model.model_ = r
        db.session.add(rule_model)
        db.session.commit()
