def boot(app):
    from views.auth.patient import patient
    from views.guest.consult import consult
    from views import base
    from views.auth import auth
    from views.auth.masterdata import masterdata
    from views.auth.model import model

    app.register_blueprint(base)
    app.register_blueprint(consult)
    app.register_blueprint(patient)
    app.register_blueprint(auth)
    app.register_blueprint(masterdata)
    app.register_blueprint(model)
