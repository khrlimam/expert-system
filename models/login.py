from werkzeug.security import generate_password_hash, check_password_hash

from boot import db


class Login(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(93))

    @property
    def password_(self):
        return self.password

    @password_.setter
    def password_(self, value):
        self.password = generate_password_hash(value)

    def check_user(self, password):
        return check_password_hash(self.password, password)
