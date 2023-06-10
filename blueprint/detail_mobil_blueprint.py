import os
from flask import Flask, Blueprint, render_template, request, redirect, flash,jsonify
from models.mobil_model import DetailMobil, Mobil, Pemesanan, MobilDisewa, Transaksi ,db
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.dirname(__file__)) + "\static\media/"

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

detail_mobil_blueprint = Blueprint("detail_mobil_blueprint", __name__)\

@detail_mobil_blueprint.route('/mobil/<id>/detail')
def detail_mobil(id):
    detail_mobil = DetailMobil.query.filter_by(mobil_id=id).all()
    return render_template('detail_mobil.html', dm=detail_mobil, id=id)

@detail_mobil_blueprint.route('/add<id>')
def add_detail(id):
    mobil = Mobil.query.filter_by(id=id).first()
    return render_template('tambah_detail.html', id=id,merek=mobil.merek,harga_sewa=mobil.harga_sewa,nomor_plat=mobil.nomor_plat)

@detail_mobil_blueprint.route('/detail/<id>/save', methods=['POST'])
def save_detail(id):
    if request.method == 'POST':
        mobil_id = id
        f_merek = request.form.get("merek")
        f_no_plat = request.form.get("nomor_plat")
        f_warna = request.form.get("warna")
        f_harga_sewa = request.form.get("harga_sewa")
        photo = request.files['Photo']
        print(photo.filename)
        if photo.filename == '':
            flash("Photo tidak boleh kosong")
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            f_photo = os.path.join('static\media', filename)
            d = DetailMobil(mobil_id=mobil_id, merek=f_merek, harga_sewa=f_harga_sewa, nomor_plat=f_no_plat, warna=f_warna, photo=f_photo)
            db.session.add(d)
            db.session.commit()
            return redirect(f'/mobil/{id}/detail')

@detail_mobil_blueprint.route('/mobil/<id>/detail/<d_id>/edit')
def edit_detail(id,d_id):
    obj = DetailMobil.query.filter_by(id=d_id).first()
    return render_template("edit_detail.html",obj=obj,d_id=d_id,id=id)

@detail_mobil_blueprint.route('/mobil/<id>/detail/<d_id>/save', methods=['POST'])
def update_detail(id,d_id):
    obj = DetailMobil.query.filter_by(id=d_id).first()
    f_merek = request.form.get("merek")
    f_no_plat = request.form.get("nomor_plat")
    f_warna = request.form.get("warna")
    f_harga_sewa = request.form.get("harga_sewa")
    photo = request.files['Photo']
    print(photo.filename)
    if photo.filename == '':
        flash("Photo tidak boleh kosong")
    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        f_photo = os.path.join('static\media', filename)

    obj.merek=f_merek
    obj.nomor_plat=f_no_plat
    obj.warna=f_warna
    obj.harga_sewa=f_harga_sewa
    obj.photo=f_photo

    #save perubahan data ke db

    db.session.add(obj)
    db.session.commit()
    return redirect(f'/mobil/{id}/detail')
  
@detail_mobil_blueprint.route("/mobil/<id>/detail/<p_id>/delete")
def delete_jurnal(id,p_id):
    p = DetailMobil.query.filter_by(id=p_id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(f'/mobil/{id}/detail')
   
  
   


ROWS_PER_PAGE = 5
@detail_mobil_blueprint.route('/pemesanan/<int:page>')
def index(page):
    

    pemesanan = Pemesanan.query.paginate(page=page, per_page=ROWS_PER_PAGE) 
    mobildip = MobilDisewa.query.paginate(page=page, per_page=ROWS_PER_PAGE) 
    kembali = Transaksi.query.all()
    return render_template('tabs.html', pemesanan=pemesanan, mdp=mobildip,lt=kembali,page=page)




@detail_mobil_blueprint.route('/lunas')
def lunas():
    # Ambil data pemesanan yang lunas dari tabel pemesanan
    data_lunas = Pemesanan.query.filter_by(status='Lunas').all()

    return render_template('index2.html', data_lunas=data_lunas)

    
@detail_mobil_blueprint.route('/belum_lunas')
def belum_lunas():
    # Ambil data pemesanan yang belum lunas dari database atau sumber data lainnya
    belum_lunas = Pemesanan.query.filter_by(status='belum lunas').all()

    return render_template('index2.html', belum_lunas=belum_lunas)




@detail_mobil_blueprint.route('/get_detail_mobil', methods=['POST'])
def get_detail_list():
    mobil_id = request.form.get('mobil_id')
    print(mobil_id)

    booking_list = DetailMobil.query.filter_by(mobil_id=mobil_id).all()

    results = []
    for booking in booking_list:
        result = {
            'merek': booking.merek,
            'nomor_plat': booking.nomor_plat,
            'warna': booking.warna,
            'harga_sewa': booking.harga_sewa,
           
        }
        results.append(result)

    return jsonify({'detail_mobil': results})
@detail_mobil_blueprint.route('/indexkuy')
def indexkuy():
    return render_template('indexkuy.html')

@detail_mobil_blueprint.route('/get_bookingkuy_mobil', methods=['POST'])
def get_booking_list():
    mobil_id = request.form.get('mobil_id')
    print(mobil_id)

    booking_list = Pemesanan.query.filter_by(mobil_id=mobil_id).all()

    results = []
    for booking in booking_list:
        result = {
            'merek': booking.merek,
            'nomor_plat': booking.nomor_plat,
            'warna': booking.warna,
            'harga_sewa': booking.harga_sewa,
            # tambahkan atribut sesuai dengan model tabel Pemesanan
            'denda_per_hari': booking.denda_per_hari,
            'jumlah_hari': booking.jumlah_hari,
            'tgl_sewa': booking.tgl_sewa.strftime('%Y-%m-%d'),
            'tgl_kembali': booking.tgl_kembali.strftime('%Y-%m-%d'),
            'total_biaya': booking.total_biaya,
            'last_updated': booking.last_updated
        }
        results.append(result)

    return jsonify({'booking_list': results})

