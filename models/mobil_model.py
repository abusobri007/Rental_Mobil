from extensions import db,UserMixin,datetime
from flask import Flask
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __repr__(self) -> str:
        return f'{self.username}>'


class Mobil(db.Model):
    id = Column(Integer, primary_key=True)
    merek = Column(String(50), nullable=False)
    harga_sewa = Column(Integer, nullable=False)
    denda_per_hari = Column(Integer, nullable=False, server_default='0')
    mobils = db.relationship('DetailMobil', backref='mobil',  cascade='save-update, merge, delete')
    mobilst = db.relationship('Pemesanan', backref='mobil',  cascade='save-update, merge, delete')
    photo = db.Column(db.String(100))
    nomor_plat = db.Column(db.String(10))
    tgl_kembali = db.Column(db.Date, nullable=True)
    last_updated = db.Column(db.String(50))

    status = db.Column(db.String(20), default='tersedia')
    
    def __repr__(self) -> str:
        return f"<{self.merek}>"
    
class DetailMobil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    merek = Column(String(50), nullable=False)
    nomor_plat = db.Column(db.String(10), nullable=False)
    warna = db.Column(db.String(10), nullable=False)
    harga_sewa = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String(100))
    mobil_id = db.Column(db.Integer, db.ForeignKey('mobil.id'))

    def __repr__(self) -> str:
        return f"<{self.warna}>"
    
class Pemesanan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.Integer, nullable=False)
    merek = Column(String(50), nullable=False)
    denda_per_hari = db.Column(db.Integer, nullable=False, server_default='0')
    harga_sewa = db.Column(db.Integer, nullable=False)
    jumlah_hari = db.Column(db.Integer, nullable=False)
    tgl_sewa = db.Column(db.DateTime, nullable=False)
    tgl_kembali = db.Column(db.DateTime, nullable=False)
    total_biaya = db.Column(db.Integer, nullable=False)
    nomor_plat = db.Column(db.String(10))
    mobil_id = db.Column(db.Integer, db.ForeignKey('mobil.id'))
    last_updated = db.Column(db.String(50))
    status_mobil = db.Column(db.String(20))

    def __repr__(self) -> str:
        return f"<{self.nama}>"


class Transaksi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.Integer, nullable=False)
    tgl_sewa = db.Column(db.DateTime)
    tgl_kembali = db.Column(db.DateTime, default=None)
    tgl_kembali_aktual = db.Column(db.DateTime)
    jumlah_hari = db.Column(db.Integer, nullable=False,server_default='0')
    metode_pembayaran = db.Column(db.String(20), nullable=False)
    total_biaya = db.Column(db.Integer, nullable=False)
    denda = db.Column(db.Integer, default=0)
    harga_sewa = db.Column(db.Integer, nullable=False, server_default='0')
    denda_per_hari = db.Column(db.Integer, nullable=False, server_default='0')
    pemesanan_id = db.Column(db.Integer, db.ForeignKey('pemesanan.id'), nullable=False)
    dp = db.Column(db.Integer)
    sisa_harga = db.Column(db.Integer)
    add_playment =  db.Column(db.Integer)
    last_updated = db.Column(db.String(50))
    status = db.Column(db.String(20))
  

    def __repr__(self) -> str:
        return f"<{self.nama}>"

class MobilDipinjam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50), nullable=False)
    merek = Column(String(50), nullable=False)
    tgl_sewa = db.Column(db.DateTime, nullable=False)
    tgl_kembali = db.Column(db.DateTime, nullable=False)
    photo = db.Column(db.String(100))
    mobil_id = db.Column(db.Integer, db.ForeignKey('mobil.id'))
    

class MobilDisewa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50), nullable=False)
    merek = Column(String(50), nullable=False)
    denda_per_hari = db.Column(db.Integer)
    harga_sewa = db.Column(db.Integer)
    jumlah_hari = db.Column(db.Integer)
    dp = db.Column(db.Integer)
    tgl_sewa = db.Column(db.DateTime, nullable=False)
    tgl_kembali = db.Column(db.DateTime, nullable=False)
    total_biaya = db.Column(db.Integer)
    nomor_plat = db.Column(db.String(10))
    sisa_harga = db.Column(db.Integer)
    status = db.Column(db.String(20))
    status_mobil = db.Column(db.String(20))                     
    filter_date = db.Column(db.DateTime)
    last_updated = db.Column(db.String(50))
    search_term = db.Column(db.String(50))
    pemesanan_id = db.Column(db.Integer, db.ForeignKey('pemesanan.id'))
