from flask import render_template, request, redirect, flash, session,Markup
import werkzeug.utils
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from app import app
from .models import db, engine, Users, Mahasiswa, Dosen, Krs, Mata_kuliah


@app.route('/', methods=['GET','POST'])
def index():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    if session.get('username'):
        mhs = Mahasiswa.query.count()
        dosen = Dosen.query.count()
        mk = Mata_kuliah.query.count()
    # users = Users.query.with_entities(Users.nik, db.func.count()).all()
        return render_template('dashboard.html',mhs=mhs,dosen=dosen,mk=mk)
    else:
        return render_template('eror.html')

@app.route('/tambah_mhs', methods=['GET', 'POST'])
def tambah_mhs():
    if request.method == 'POST':
        npm = request.form['npm']
        nama = request.form['nama']
        tmpt_lahir = request.form['tmpt_lahir']
        tgl_lahir = request.form['tgl_lahir']
        alamat = request.form['alamat']
        jurusan = request.form['jurusan']
        thn_masuk = request.form['thn_masuk']
        try:
            addMhs = Mahasiswa(npm=npm,nama=nama,tmpt_lahir=tmpt_lahir,tgl_lahir=tgl_lahir,
              alamat=alamat,jurusan=jurusan, thn_masuk=thn_masuk)
            db.session.add(addMhs)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)
        # berhasil = Markup('<p class="alert alert-success" style="color:black">Data Berhasil Diinputkan</p>')
        # flash(berhasil)
    # listMhs = Mahasiswa.query.all()
    # print(listMhs)
    return render_template('mahasiswa/tambah_mhs.html')
#
@app.route('/lihat_mhs')
def lihat_mhs():
    if session.get('username'):
        mhs = Mahasiswa.query.all()
        return render_template('mahasiswa/lihat_mhs.html', mhs=mhs)
    else:
        return render_template('eror.html')

@app.route('/edit_mhs/<int:npm>')
def updateForm(npm):
    mhs = Mahasiswa.query.filter_by(npm=npm).first()
    return render_template("mahasiswa/edit_mhs.html", data=mhs)
#
@app.route('/edit_mhs', methods=['POST'])
def update():
    if request.method == 'POST':
        # id = request.form['id']
        npm = request.form['npm']
        nama = request.form['nama']
        tmpt_lahir = request.form['tmpt_lahir']
        tgl_lahir = request.form['tgl_lahir']
        alamat = request.form['alamat']
        jurusan = request.form['jurusan']
        thn_masuk = request.form['thn_masuk']
        try:
            mhs = Mahasiswa.query.filter_by(npm=npm).first()
            mhs.npm = npm
            mhs.nama = nama
            mhs.tmpt_lahir = tmpt_lahir
            mhs.tgl_lahir = tgl_lahir
            mhs.alamat = alamat
            mhs.jurusan = jurusan
            mhs.thn_masuk = thn_masuk
            db.session.commit()

        except Exception as e:
            print("Failed to update data")
            print(e)
        return redirect("/lihat_mhs")
#
@app.route('/hapus_mhs/<int:npm>')
def hapus_mhs(npm):
    try:
        mhs = Mahasiswa.query.filter_by(npm=npm).first()
        db.session.delete(mhs)
        db.session.commit()

    except Exception as e:
        print("Failed delete mahasiswa")
        print(e)
    return redirect("/lihat_mhs")

@app.route('/tambah_dosen', methods=['GET', 'POST'])
def tambah_dosen():
    if request.method == 'POST':
        nip = request.form['nip']
        nama = request.form['nama']
        alamat = request.form['alamat']
        no_tlp = request.form['no_tlp']
        try:
            addDosen = Dosen(nip=nip,nama=nama, alamat=alamat, no_tlp=no_tlp)
            db.session.add(addDosen)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)

    return render_template('dosen/tambah_dosen.html')
#
@app.route('/lihat_dosen')
def lihat_dosen():
    if session.get('username'):
        dosen = Dosen.query.all()
        return render_template('dosen/lihat_dosen.html', data=dosen)
    else:
        return render_template('eror.html')
#
@app.route('/hapus_dosen/<int:nip>')
def hapus_dosen(nip):
    try:
        dosen = Dosen.query.filter_by(nip=nip).first()
        db.session.delete(dosen)
        db.session.commit()

    except Exception as e:
        print("Failed delete mahasiswa")
        print(e)
    return redirect("/lihat_dosen")

@app.route('/edit_dosen/<int:nip>')
def dosenForm(nip):
    dosen = Dosen.query.filter_by(nip=nip).first()
    return render_template("dosen/edit_dosen.html", data=dosen)
#
@app.route('/edit_dosen', methods=['POST'])
def edit_dosen():
    if request.method == 'POST':
        nip = request.form['nip']
        nama = request.form['nama']
        alamat = request.form['alamat']
        no_tlp = request.form['no_tlp']
        try:
            dosen = Dosen.query.filter_by(nip=nip).first()
            dosen.nip = nip
            dosen.nama = nama
            dosen.alamat = alamat
            dosen.no_tlp = no_tlp
            db.session.commit()

        except Exception as e:
            print("Failed to update data")
            print(e)
        return redirect("/lihat_dosen")
@app.route('/tambah_mk', methods=['GET', 'POST'])
def tambah_mk():
    if request.method == 'POST':
        kode_mk = request.form['kode_mk']
        makul = request.form['makul']
        sks = request.form['sks']
        try:
            mk = Mata_kuliah(kode_mk=kode_mk, makul=makul, sks=sks)
            db.session.add(mk)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)

    return render_template('matakuliah/tambah_mk.html')

@app.route('/lihat_mk')
def lihat_mk():
    if session.get('username'):
        mk = Mata_kuliah.query.all()
        return render_template('matakuliah/lihat_mk.html', mk=mk)
    else:
        return render_template('eror.html')

@app.route('/hapus_mk/<int:kode_mk>')
def hapus_mk(kode_mk):
    try:
        mk = Mata_kuliah.query.filter_by(kode_mk=kode_mk).first()
        db.session.delete(mk)
        db.session.commit()

    except Exception as e:
        print("Failed delete mahasiswa")
        print(e)
    return redirect("/lihat_mk")

@app.route('/edit_mk/<int:kode_mk>')
def mkForm(kode_mk):
    mk = Mata_kuliah.query.filter_by(kode_mk=kode_mk).first()
    return render_template("matakuliah/edit_mk.html", data=mk)
#
@app.route('/edit_mk', methods=['POST'])
def edit_mk():
    if request.method == 'POST':
        kode_mk = request.form['kode_mk']
        makul = request.form['makul']
        sks = request.form['sks']
        try:
            mk = Mata_kuliah.query.filter_by(kode_mk=kode_mk).first()
            mk.kode_mk = kode_mk
            mk.makul = makul
            mk.sks = sks
            db.session.commit()

        except Exception as e:
            print("Failed to update data")
            print(e)
        return redirect("/lihat_mk")

@app.route('/tambah_krs', methods=['GET', 'POST'])
def tambah_krs():
    mhs = Mahasiswa.query.all()
    mk = Mata_kuliah.query.all()
    dosen = Dosen.query.all()
    if request.method == 'POST':
        npm = request.form['npm']
        kode_mk = request.form['kode_mk']
        kode_dosen = request.form['kode_dosen']
        nilai_uts = request.form['nilai_uts']
        nilai_uas = request.form['nilai_uas']
        kelas = request.form['kelas']
        thn_ajaran = request.form['thn_ajaran']
        nilai_ipk = request.form['nilai_ipk']
        try:
            addKrs = Krs(npm=npm,kode_mk=kode_mk,kode_dosen=kode_dosen,
            nilai_uts=nilai_uts, nilai_uas=nilai_uas, kelas=kelas,thn_ajaran=thn_ajaran, nilai_ipk=nilai_ipk)
            db.session.add(addKrs)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)

    return render_template('krs/tambah_krs.html',mhs=mhs, mk=mk,dosen=dosen)

@app.route('/lihat_krs')
def lihat_krs():
    if session.get('username'):
        krs = Krs.query.all()
        return render_template('krs/lihat_krs.html', krs=krs)
    else:
        return render_template('eror.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password = password.strip()
        hashed_pwd = generate_password_hash(password, 'sha256')
        try:
            adduser = Users(username=username,pass_hash=hashed_pwd)
            db.session.add(adduser)
            db.session.commit()
        except Exception as e:
            print("Failed to add data.")
            print(e)
    # listMhs = Mahasiswa.query.all()
    # print(listMhs)
    return render_template('register.html')

@app.route('/data_user')
def data_user():
    if session.get('username'):
        users = Users.query.all()
        return render_template('lihat_user.html', users=users)
    else:
        return render_template('eror.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not (username and password):
            kosong = Markup('<p class="alert alert-warning" style="color:black">Username atau Password tidak boleh kosong</p>')
            flash(kosong)
            return redirect('/login')
        else:
            username = username.strip()
            password = password.strip()
        user = Users.query.filter_by(username=username).first()
        if user and check_password_hash(user.pass_hash, password):
            session['username'] = username
            return redirect("/dashboard")
        else:
            invalid = Markup('<p class="alert alert-danger" style="color:black">Username atau password salah</>')
            flash(invalid)

    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect('/')
