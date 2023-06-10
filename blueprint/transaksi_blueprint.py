from flask import Flask ,  session
from flask import Blueprint ,render_template,request,  redirect,flash
from models.mobil_model import Transaksi, Pemesanan, Mobil, MobilDisewa,db 
from werkzeug.utils import secure_filename
from datetime import datetime,timedelta,date

transaksi_blueprint = Blueprint("transaksi_blueprint", __name__)

@transaksi_blueprint.route('/pemesanan/<id>/transaksi')
def list_pemesanan(id):
    list_transaksi = Transaksi.query.filter_by(pemesanan_id=id).all()
    return render_template('transaksi.html', lt=list_transaksi, id=id)
ROWS_PER_PAGE = 5
@transaksi_blueprint.route('/list_pengembalian/<int:page>')
def all_transaksi(page):
    transaksi = Transaksi.query.paginate(page=page, per_page=ROWS_PER_PAGE)  
    return render_template('transaksi.html',  transaksi=transaksi,page=page)

@transaksi_blueprint.route('/add_transaksi/<id>')
def add_transaksi(id):
    pemesanan = MobilDisewa.query.filter_by(id=id).first()
    if pemesanan.status_mobil == 'dipinjam':
       pemesanan.status_mobil = 'kembali'
       db.session.commit()
       flash('Mobil berhasil dikembalikan.', 'success')
    else:
        flash('Mobil tidak dalam status dipinjam.', 'error')
    
    return render_template('add_transaksi.html', id=id,
                               jumlah_hari=pemesanan.jumlah_hari,nama=pemesanan.nama,harga_sewa=pemesanan.harga_sewa,
                               denda_per_hari=pemesanan.denda_per_hari, dp=pemesanan.dp,tgl_sewa=pemesanan.tgl_sewa, tgl_kembali=pemesanan.tgl_kembali,total_biaya=pemesanan.total_biaya,
                               sisa_harga=pemesanan.sisa_harga)
@transaksi_blueprint.route('/transaksi/<id>/save', methods=['POST'])
def save_transaksi(id):
      if request.method == 'POST':
        pemesanan = MobilDisewa.query.filter_by(id=id).first()
        nama = request.form.get('nama')
        tgl_sewa = datetime.strptime(request.form['tgl_sewa'], '%Y-%m-%d')
        tgl_kembali = datetime.strptime(request.form['tgl_kembali'], '%Y-%m-%d')
        tgl_kembali_aktual = datetime.strptime(request.form['tgl_kembali_aktual'], '%Y-%m-%d')
        metode_pembayaran = request.form.get('metode_pembayaran')
        dateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            jumlah_hari = int(request.form.get('jumlah_hari'))
        except ValueError:
            jumlah_hari = 0

        try:
            dp = int(request.form.get('dp'))
        except ValueError:
            dp = 0

        try:
            harga_sewa = int(request.form.get('harga_sewa'))
        except ValueError:
            harga_sewa = 0

        try:
            sisa_harga = int(request.form.get('sisa_harga'))
        except ValueError:
            sisa_harga = 0

        add_playment = request.form.get('add_playment')
        if add_playment is not None:
           try:
            add_playment = int(add_playment)
           except ValueError:
            add_playment = 0
        else:
         add_playment = 0

        try:
            denda_per_hari = int(request.form.get('denda_per_hari'))
        except ValueError:
            denda_per_hari = 0

        denda = 0  # Inisialisasi denda dengan nilai awal 0

        try:
            total_biaya = harga_sewa * jumlah_hari
        except ValueError:
            total_biaya = 0

        if tgl_kembali_aktual > pemesanan.tgl_kembali:
            selisih_hari = (tgl_kembali_aktual - pemesanan.tgl_kembali).days
            denda = selisih_hari * denda_per_hari
            total_biaya += denda

        total_biaya -= dp
        sisa_harga = total_biaya - add_playment
 

        # Melanjutkan logika lainnya...


        transaction = Transaksi(pemesanan_id=id, nama=nama, tgl_sewa=tgl_sewa,
                        tgl_kembali=tgl_kembali, metode_pembayaran=metode_pembayaran, harga_sewa=harga_sewa, denda_per_hari=denda_per_hari,
                        denda=denda, total_biaya=total_biaya, jumlah_hari=jumlah_hari,dp=dp,sisa_harga=sisa_harga,
                        tgl_kembali_aktual=tgl_kembali_aktual,add_playment=add_playment,last_updated=dateNow)

        db.session.add(transaction)
        db.session.commit()

        return redirect('/list_pengembalian/1')
    


@transaksi_blueprint.route("/transaksi/<id>/delete")
def delete_transaksi(id):
    p = Transaksi.query.filter_by(id=id).first()
    db.session.delete(p)
    db.session.commit()
   
    return redirect(f'/list_pengembalian/1')

@transaksi_blueprint.route('/transaksi/<id>/edit')
def edit_transaksi(id):
    obj = Transaksi.query.filter_by(id).first()
    return render_template("edit_transaksi.html",obj=obj,id=id)
@transaksi_blueprint.route('/transaksi/id>/save', methods=['POST'])
def update_transaksi(id):
    obj = Transaksi.query.filter_by(id=id).first()
    f_nama = request.form.get('nama')
    tanggal_transaksi = datetime.strptime(request.form['tanggal_transaksi'], '%Y-%m-%d')
    tgl_kembali = datetime.strptime(request.form['tgl_kembali'], '%Y-%m-%d')
    metode_pembayaran = request.form.get('metode_pembayaran')
    dateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        jumlah_hari = int(request.form.get('jumlah_hari'))
    except ValueError:
        jumlah_hari = 0
    try:
        harga_sewa = int(request.form.get('harga_sewa'))
    except ValueError:
        harga_sewa = 0
    try:
        denda_per_hari = int(request.form.get('denda_per_hari'))
    except ValueError:
        denda_per_hari = 0
    try:
        total_biaya = int(request.form.get('total_biaya'))
    except ValueError:
        total_biaya = 0
    
    obj.nama = f_nama
    obj.tanggal_transaksi = tanggal_transaksi
    obj.tgl_kembali = tgl_kembali
    obj.metode_pembayaran = metode_pembayaran
    obj.jumlah_hari = jumlah_hari
    obj.harga_sewa = harga_sewa
    obj.denda_per_hari = denda_per_hari
    obj.total_biaya = total_biaya
    obj.last_updated = dateNow
    db.session.add(obj)
    db.session.commit()
    return redirect(f'/list_pengembalian/1')
 
   
