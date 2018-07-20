from flask import Blueprint

consult = Blueprint('consult', __name__, url_prefix='/consult')


@consult.route('/')
def index():
    return 'Josh Gandosh!'
