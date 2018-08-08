from flask import Blueprint, request, redirect, url_for, flash
from flask import render_template

from boot import db
from models.gejala import Gejala
from models.penyakit import Penyakit
from views.auth import auth_group, login_required

masterdata = Blueprint('master', __name__, url_prefix=auth_group('data'))


@masterdata.route('penyakit', methods=['GET', 'POST', 'PATCH'])
@login_required
def penyakit():
    if request.method == 'GET':
        penyakits = Penyakit.query.all()
        return render_template('auth/penyakit/index.html', penyakits=penyakits)
    if request.method == 'POST':
        penyakit = Penyakit()
        method = request.form.get('method', '')
        nama_penyakit = request.form.get('nama')
        if method == 'PATCH':
            penyakit_id = request.form.get('id')
            penyakit = Penyakit.query.get_or_404(penyakit_id)
            flash('Data penyakit %s telah disimpan' % nama_penyakit)
        penyakit.nama = nama_penyakit
        if method != 'PATCH':
            db.session.add(penyakit)
            flash('Data penyakit %s telah ditambahkan' % penyakit.nama)
        db.session.commit()
        return redirect(url_for('master.penyakit'))


@masterdata.route('/penyakit/<int:id>/delete')
@login_required
def delete_penyakit(id):
    penyakit = Penyakit.query.get_or_404(id)
    penyakit_nama = penyakit.nama
    db.session.delete(penyakit)
    db.session.commit()
    flash('Data penykait %s berhasil dihapus!' % penyakit_nama)
    return redirect(url_for('master.penyakit'))


@masterdata.route('/gejala/<int:id>/delete')
@login_required
def delete_gejala(id):
    gejala = Gejala.query.get_or_404(id)
    gejala_nama = gejala.nama
    db.session.delete(gejala)
    db.session.commit()
    flash('Data penykait %s berhasil dihapus!' % gejala_nama)
    return redirect(url_for('master.gejala'))


@masterdata.route('gejala', methods=['GET', 'POST', 'PATCH'])
@login_required
def gejala():
    if request.method == 'GET':
        gejalas = Gejala.query.all()
        return render_template('auth/gejala/index.html', gejalas=gejalas)
    if request.method == 'POST':
        gejala = Gejala()
        method = request.form.get('method', '')
        nama_gejala = request.form.get('nama')
        if method == 'PATCH':
            gejala_id = request.form.get('id')
            gejala = Gejala.query.get_or_404(gejala_id)
            flash('Data gejala %s telah disimpan' % nama_gejala)
        gejala.nama = nama_gejala
        if method != 'PATCH':
            db.session.add(gejala)
            flash('Data gejala %s telah ditambahkan' % gejala.nama)
        db.session.commit()
        return redirect(url_for('master.gejala'))
