import os
from flask import Flask
from flask import Blueprint ,render_template,request,  redirect,flash
from models.mobil_model import Mobil,Pemesanan, MobilDisewa, db
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user 
from datetime import datetime

app = Flask(__name__)


app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.dirname(__file__)) + "\static\media/"
ALLOWED_EXTENSIONS = { 'pdf', 'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

mobil_blueprint = Blueprint("mobil_blueprint", __name__)\

@mobil_blueprint.route('/tentang_kami')
def tentang_kami():
    return render_template('tentang_kami.html')
@mobil_blueprint.route('/sewa', methods=['GET', 'POST'])
def sewa():
    if request.method == 'POST':
        # Ambil tanggal sewa dan tanggal kembali dari form
        tgl_sewa = datetime.strptime(request.form['tgl_sewa'], '%Y-%m-%d').date()
        tgl_kembali = datetime.strptime(request.form['tgl_kembali'], '%Y-%m-%d').date()

        # Ambil semua mobil yang tersedia pada rentang tanggal sewa dan tanggal kembali
        pemesanan_query = db.session.query(Pemesanan.mobil_id).filter(
            (Pemesanan.tgl_sewa <= tgl_sewa) & (Pemesanan.tgl_kembali >= tgl_sewa) |
            (Pemesanan.tgl_sewa <= tgl_kembali) & (Pemesanan.tgl_kembali >= tgl_kembali) |
            (Pemesanan.tgl_sewa >= tgl_sewa) & (Pemesanan.tgl_kembali <= tgl_kembali)
        )
        mobils = Mobil.query.filter(~Mobil.id.in_(pemesanan_query), Mobil.status == 'tersedia').all()

        # Tambahkan informasi tanggal sewa dan tanggal kembali ke dalam konteks
        context = {
            'mobils': mobils,
            'tgl_sewa': tgl_sewa,
            'tgl_kembali': tgl_kembali,
            'reserved_dates': []
        }

        # Ambil semua tanggal yang sudah dipesan pada rentang tanggal sewa dan tanggal kembali
        pemesanan = Pemesanan.query.filter(
            (Pemesanan.tgl_sewa <= tgl_sewa) & (Pemesanan.tgl_kembali >= tgl_sewa) |
            (Pemesanan.tgl_sewa <= tgl_kembali) & (Pemesanan.tgl_kembali >= tgl_kembali) |
            (Pemesanan.tgl_sewa >= tgl_sewa) & (Pemesanan.tgl_kembali <= tgl_kembali)
        ).all()

        # Tambahkan tanggal yang sudah dipesan ke dalam daftar tanggal yang sudah dipesan
        for p in pemesanan:
            reserved_dates = [d.strftime('%Y-%m-%d') for d in p.get_dates()]
            context['reserved_dates'].extend(reserved_dates)

        # Kirimkan konteks ke halaman template
        return render_template('home.html', **context)

    # Jika metode HTTP adalah GET, tampilkan halaman sewa
    return render_template('home.html')


from datetime import datetime

from operator import itemgetter

# ...

@mobil_blueprint.route('/detail_mobil')
@login_required


def detail_mobil():
    mobil_dict = {}
    mobils = Mobil.query.all()
    mobil_dipinjam = []
    tgl_sewa_filter = datetime.strptime(request.args.get('tgl_sewa'), '%Y-%m-%d').date() if request.args.get('tgl_sewa') else None

    for mobil in mobils:
        if mobil.status == 'Tersedia':
            mobil_dict[mobil] = {'status': 'Tersedia', 'class': 'bg-success'}
        else:
            pesanan = Pemesanan.query.filter_by(mobil_id=mobil.id).filter(Pemesanan.tgl_kembali > datetime.now()).first()
            if pesanan and pesanan.tgl_sewa <= datetime.now():
                mobil_dipinjam.append(mobil)
            else:
                mobil_dict[mobil] = {'status': 'Tersedia', 'class': 'bg-success'}

    # Menambahkan mobil yang sedang dipinjam di bagian atas mobil_dict
    for mobil in mobil_dipinjam:
        mobil_dict[mobil] = {'status': 'Dipinjam', 'class': 'bg-danger'}

    if tgl_sewa_filter:
        mobil_dict = {mobil: info for mobil, info in mobil_dict.items() if pesanan and pesanan.tgl_sewa.date() == tgl_sewa_filter}

    return render_template('mobil.html', mobil_dict=mobil_dict)


@mobil_blueprint.route('/list_mobil', methods=['GET', 'POST'])

def list_mobil():
    if request.method == 'POST':
        # Ambil tanggal sewa dan tanggal kembali dari form
        tgl_sewa = datetime.strptime(request.form['tgl_sewa'], '%Y-%m-%d').date()
        
        tgl_kembali = datetime.strptime(request.form['tgl_kembali'], '%Y-%m-%d').date()

       # Ambil semua mobil yang tersedia pada rentang tanggal sewa dan tanggal kembali
        pemesanan_query = db.session.query(Pemesanan.mobil_id).filter(
        (Pemesanan.tgl_sewa <= tgl_sewa) & (Pemesanan.tgl_kembali >= tgl_sewa) | #memeriksa apakah tgl_sewa berada di antara tgl_sewa dan tgl_kembali dari suatu pemesanan mobil atau tidak.
        (Pemesanan.tgl_sewa <= tgl_kembali) & (Pemesanan.tgl_kembali >= tgl_kembali) |
        (Pemesanan.tgl_sewa >= tgl_sewa) & (Pemesanan.tgl_kembali <= tgl_kembali)#memeriksa apakah rentang waktu pemesanan mobil berada di antara tanggal tgl_sewa dan tgl_kembali yang dimasukkan atau tidak.
        )
        mobils = Mobil.query.filter(~Mobil.id.in_(pemesanan_query), Mobil.status == 'tersedia').all()

    
        return render_template('mobil2.html', mobils=mobils,tgl_sewa=tgl_sewa)
    
    


@mobil_blueprint.route('/add')
def add_mobil():
    return  render_template("tambah_mobil.html")

@mobil_blueprint.route('/get-form', methods=['GET'])
def get_form():
    return '''
        <div class="container">
            <div class="row">
                <div class="col"></div>
                <div class="col">
                    <h1 class="fw-bolder:center">Tambah Mobil</h1>
                    <form>
                        <div class="form-group">
                            <label for="merek">Merek</label>
                            <input type="text" name="merek" id="merek" class="form-control" value="">
                        </div>
                        <div class="form-group">
                            <label for="harga_sewa">Harga Sewa</label>
                            <input type="number" name="harga_sewa" id="harga_sewa" class="form-control">
                        </div>
                        <div class="form-group">
                            <label for="Photo">File</label>
                            <input type="file" name="Photo" id="Photo" class="form-control">
                        </div>
                        <div class="form-group">
                            <a href="/detail_mobil" class="btn btn-warning">Cancel</a>
                            <button class="btn btn-secondary">Submit</button>
                        </div>
                    </form>
                </div>
                <div class="col"></div>
            </div>
        </div>
    '''



@mobil_blueprint.route("/add_mobil/save", methods=['POST'])
def save_mobil():
    if request.method == 'POST':

       f_merek =request.form.get("merek")
       f_harga_sewa =request.form.get("harga_sewa")
       f_denda =request.form.get("denda_per_hari")
       
       photo = request.files['Photo']
       print(photo.filename)
       if photo.filename== '':
           flash("Photo tidak boleh kosong")
       if photo and allowed_file(photo.filename):
          filename= secure_filename(photo.filename)
          photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          f_photo = os.path.join('static\media', filename)
          m= Mobil(merek=f_merek, harga_sewa=f_harga_sewa, denda_per_hari= f_denda, photo= f_photo)
       
          db.session.add(m)
          db.session.commit()
    return redirect('/detail_mobil')
       

@mobil_blueprint.route('/edit/<id>/mobil', methods=['GET', 'POST'])
def edit_mobil(id):
    obj = Mobil.query.filter_by(id=id).first()
    return render_template("edit_mobil.html", obj=obj)




@mobil_blueprint.route('/edit/<id>/save', methods=['POST'])
def update_mobil(id):
    obj = Mobil.query.filter_by(id=id).first()
    f_merek = request.form.get("merek")
    f_harga_sewa = request.form.get("harga_sewa")
    f_status = request.form.get("status")
    f_denda = request.form.get("denda_per_hari")
    f_no_plat = request.form.get("nomor_plat")
    dateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    photo = request.files['Photo']
    print(photo.filename)
    if photo.filename== '':
           flash("Photo tidak boleh kosong")
    if photo and allowed_file(photo.filename):
          filename= secure_filename(photo.filename)
          photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          f_photo = os.path.join('static\media', filename)
    obj.photo = f_photo

    obj.merek = f_merek
    obj.harga_sewa = f_harga_sewa
    obj.status = f_status
    obj.denda_per_hari = f_denda
    obj.nomor_plat = f_no_plat
    obj.last_updated = dateNow

    # save perubahan data ke db
    db.session.add(obj)
    db.session.commit()

    return redirect('/detail_mobil')



@mobil_blueprint.route("/mobil/<id>/delete")
def delete_mobil(id):
    m = Mobil.query.filter_by(id=id).first()
    db.session.delete(m)
    db.session.commit()
    return redirect(f'/detail_mobil')
  




@mobil_blueprint.route('/mobil/<id>/dipinjam')
def mobil_dipinjam(id):
    mobildp = MobilDisewa.query.filter_by(pemesanan_id=id).all()
    return render_template('mobil_dipinjam.html', dp=mobildp, id=id)


@mobil_blueprint.route("/mobil_dipinjam")
def all_mobildipinjam():
    mdp = MobilDisewa.query.all()
    return render_template('mobil_dipinjam.html',  dp=mdp)

@mobil_blueprint.route('/add_mobildipinjam/<id>')
def add_mobildipinjam(id):
     pemesanan = Pemesanan.query.filter_by(id=id).first()
    
     return render_template('add_mobildipinjam.html', id=id,
                            nama=pemesanan.nama, merek=pemesanan.merek,
                            tgl_sewa=pemesanan.tgl_sewa, tgl_kembali=pemesanan.tgl_kembali,
                            nomor_plat=pemesanan.nomor_plat,dp=pemesanan.dp,denda_per_hari=pemesanan.denda_per_hari,total_biaya=pemesanan.total_biaya,
                            jumlah_hari=pemesanan.jumlah_hari,harga_sewa=pemesanan.harga_sewa)


@mobil_blueprint.route("/add_mobildipinjam/save", methods=['POST'])
def save_mobildipinjam():
    if request.method == 'POST':
      
       f_nama =request.form.get("nama")
       f_merek =request.form.get("merek")
       nomor_plat =request.form.get("nomor_plat")
    try:
            denda_per_hari = int(request.form.get('denda_per_hari'))
    except ValueError:
            denda_per_hari = 0
    try:
            dp = int(request.form.get('dp'))
    except ValueError:
            dp = 0
    try:
           harga_sewa = int(request.form.get('harga_sewa'))
    except ValueError:
           harga_sewa = 0

    try:
           jumlah_hari = int(request.form.get('jumlah_hari'))
    except ValueError:
           jumlah_hari = 0
      
    tgl_sewa = datetime.strptime(request.form['tgl_sewa'], '%Y-%m-%d')
    tgl_kembali = datetime.strptime(request.form['tgl_kembali'], '%Y-%m-%d')
    try:
           total_biaya = int(request.form.get('total_biaya'))
    except ValueError:
           total_biaya = 0
       
    mdp= MobilDisewa( nama=f_nama, merek=f_merek,
                              harga_sewa=harga_sewa, jumlah_hari=jumlah_hari,
                              tgl_sewa=tgl_sewa, tgl_kembali=tgl_kembali,
                              total_biaya=total_biaya, 
                              denda_per_hari=denda_per_hari, nomor_plat=nomor_plat,dp=dp)
       
    db.session.add(mdp)
    db.session.commit()
    return redirect('/pemesanan/1')

@mobil_blueprint.route("/mobildipinjam/<id>/delete")
def delete_mobildipinjam(id):
    mdp = MobilDisewa.query.filter_by(id=id).first()
    db.session.delete(mdp)
    db.session.commit()
    return redirect(f'/mobil_dipinjam') 

@mobil_blueprint.route('/get-filter', methods=['GET'])
def get_filter():
    return '''
        <div class="container">
            <div class="row">
                <div class="col"></div>
                <div class="col">
                    <h1 class="fw-bolder:center">Filter Tanggal</h1>
                     <form action="/list_mobil" method="post">
                    <form>
                        <div class="form-group">
                            <label for="">tanggal sewa</label>
                            <input type="date" name="tgl_sewa" id="tgl_sewa" class="form-control" value="">
                        </div>
                         <div class="form-group">
                            <label for="">tanggal kembali</label>
                            <input type="date" name="tgl_kembali" id="tgl_kembali" class="form-control" value="">
                        </div>
                       
                        <div class="form-group">
                            <a href="/detail_mobil" class="btn btn-warning">Cancel</a>
                            <button class="btn btn-secondary">Submit</button>
                        </div>
                    </form>
                </div>
                <div class="col"></div>
            </div>
        </div>
    '''






