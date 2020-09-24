from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, table, column, func
import os
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "db_krs.db"))
engine = create_engine(database_file)

from app import app
db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'tb_pengguna'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    pass_hash = db.Column(db.String, nullable=False)
    # level     = db.Column(db.Integer, nullable=False)


class Mahasiswa(db.Model):
    __tablename__ = 'mahasiswa'

    id      = db.Column(db.Integer, primary_key=True)
    npm     = db.Column(db.Integer, nullable=False)
    nama    = db.Column(db.String, nullable=False)
    tmpt_lahir = db.Column(db.String, nullable=False)
    tgl_lahir = db.Column(db.String, nullable=False)
    alamat = db.Column(db.String, nullable=False)
    jurusan = db.Column(db.String, nullable=False)
    thn_masuk = db.Column(db.String, nullable=False)

class Dosen(db.Model):
    __tablename__ = 'dosen'

    nip      = db.Column(db.Integer, primary_key=True)
    nama    = db.Column(db.String, nullable=False)
    alamat    = db.Column(db.String, nullable=False)
    no_tlp     = db.Column(db.Integer, nullable=False)


class Mata_kuliah(db.Model):
    __tablename__ = 'mata_kuliah'

    kode_mk      = db.Column(db.Integer, primary_key=True)
    makul    = db.Column(db.String, nullable=False)
    sks     = db.Column(db.Integer, nullable=False)

class Krs(db.Model):
    __tablename__ = 'krs'

    id_krs      = db.Column(db.Integer, primary_key=True)
    npm      = db.Column(db.Integer, db.ForeignKey('mahasiswa.npm'))
    kode_mk    = db.Column(db.Integer, db.ForeignKey('mata_kuliah.kode_mk'))
    kode_dosen      = db.Column(db.Integer, db.ForeignKey('dosen.nip'))
    # kode_dosen    = db.Column(db.String, nullable=False)
    nilai_uts    = db.Column(db.String, nullable=False)
    nilai_uas    = db.Column(db.String, nullable=False)
    kelas    = db.Column(db.String, nullable=False)
    thn_ajaran    = db.Column(db.String, nullable=False)
    nilai_ipk    = db.Column(db.String, nullable=False)


db.create_all()
