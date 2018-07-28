from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from boot import app, db
from seeds import seed as _

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


from models.penyakit import Penyakit
from models.gejala import Gejala
from models.patients import Patients
from models.rule_model import RuleModel


@manager.command
def seed():
    _.start()


if __name__ == '__main__':
    manager.run()
