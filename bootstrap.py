def boot(app):
    from views.auth.patient import patient
    from views.guest.consult import consult

    app.register_blueprint(consult)
    app.register_blueprint(patient)
