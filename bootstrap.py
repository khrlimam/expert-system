def boot(app):
    from views.admin.patient_profile import patient_profile
    from views.patient.consult import consult

    app.register_blueprint(consult)
    app.register_blueprint(patient_profile)
