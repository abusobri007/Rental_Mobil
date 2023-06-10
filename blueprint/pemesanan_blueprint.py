import os,pdfkit,jinja2
from flask import Flask ,  session,render_template_string,send_file,make_response,jsonify
from flask import Blueprint ,render_template,request,  redirect,flash
from models.mobil_model import Pemesanan,Mobil, MobilDisewa, db
from werkzeug.utils import secure_filename
from datetime import datetime,timedelta,date
from fpdf import FPDF
from sqlalchemy import and_


pemesanan_blueprint = Blueprint("pemesanan_blueprint", __name__)
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


@pemesanan_blueprint.route('/get_booking_list', methods=['POST'])
def get_booking_list():
    mobil_id = request.form.get('mobil_id')
    print(mobil_id)

    booking_list = Pemesanan.query.filter_by(mobil_id=mobil_id).all()

    results = []
    for booking in booking_list:
        result = {
            'nama': booking.nama,
            'merek': booking.merek,
            'nomor_plat': booking.nomor_plat,
            'denda_per_hari': booking.denda_per_hari,
            'harga_sewa': booking.harga_sewa,
            'jumlah_hari': booking.jumlah_hari,
            'tgl_sewa': booking.tgl_sewa,
            'tgl_kembali': booking.tgl_kembali,
            'total_biaya': booking.total_biaya,
            
        }
        results.append(result)
    
    return jsonify({'booking_list': results})





@pemesanan_blueprint.route('/mobil/<id>/pemesanan', methods=['GET', 'POST'])
def list_pemesanan(id):
    if request.method == 'POST':
        # Code untuk memproses data yang dikirimkan melalui AJAX POST request
        # ...
        return jsonify(success=True)

    # Jika request adalah GET, maka tampilkan halaman template pemesanan.html
    list_pemesanan = Pemesanan.query.filter_by(mobil_id=id).all()
    return render_template('pemesanan.html', lp=list_pemesanan, id=id)




ROWS_PER_PAGE = 4

@pemesanan_blueprint.route('/list_pesanan/<int:page>', methods=['GET', 'POST'])
def all_pesan(page):
  
        status_mobil = request.args.get('status_mobil')
     
       
        mdp = Pemesanan.query

        if status_mobil:
         if status_mobil == 'dibooking' or status_mobil == 'Dibatalkan':
            mdp = mdp.filter(Pemesanan.status_mobil == status_mobil)
        elif status_mobil == 'semua':
            # Tidak ada filter pada status_mobil, tampilkan semua data
            pass

       
    

        pemesanan = mdp.paginate(page=page, per_page=ROWS_PER_PAGE)
    
        return render_template('booking.html', pemesanan=pemesanan, page=page)


from sqlalchemy import or_

ROWS_PER_PAGE = 4
@pemesanan_blueprint.route('/list_transaksikuy/<int:page>')
def all_pemesanan(page):
    tr = MobilDisewa.query.all()

    for a in tr:
        if a.sisa_harga != 0 and a.status is not None and not a.status.endswith('belum lunas'):
            a.status += 'belum lunas'
            db.session.add(a)
            db.session.commit()

    status_mobil = request.args.get('status_mobil')
    statusPemesanan = request.args.get('status')
    filter_date = request.args.get('filter_date', '')
    search_term = request.args.get('merek_nama')

    mdp = MobilDisewa.query

    if status_mobil:
        if status_mobil == 'dipinjam' or status_mobil == 'kembali':
            mdp = mdp.filter(MobilDisewa.status_mobil == status_mobil)
        elif status_mobil == 'semua':
            # Tidak ada filter pada status_mobil, tampilkan semua data
            pass

    if statusPemesanan:
        if statusPemesanan != 'semua':
            mdp = mdp.filter_by(status=statusPemesanan)

    if filter_date:
        filter_date = datetime.strptime(filter_date, '%Y-%m-%d')
        mdp = mdp.filter(and_(MobilDisewa.tgl_sewa <= filter_date, MobilDisewa.tgl_kembali >= filter_date))

    if search_term:
        mdp = mdp.filter(or_(MobilDisewa.merek.ilike(f'%{search_term}%'), MobilDisewa.nama.ilike(f'%{search_term}%')))


    transaksi_paginated = mdp.paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('pemesanan.html', mdp=transaksi_paginated, page=page,search_term=search_term)


@pemesanan_blueprint.route('/add_pemesanan/<int:id>')
def add_pemesanan(id):
    mobil = Mobil.query.get(id)

    # Dapatkan data pemesanan mobil yang sudah ada
    pemesanan_mobil = Pemesanan.query.filter_by(mobil_id=id).all()

    # Buat daftar tanggal sewa yang sudah dipesan
    booked_dates = []
    for pemesanan in pemesanan_mobil:
        durasi = (pemesanan.tgl_kembali - pemesanan.tgl_sewa).days + 1
        for i in range(durasi):
            tanggal_sewa = pemesanan.tgl_sewa + timedelta(days=i)
            if i < durasi - 1:  # Hanya tambahkan tanggal sewa hingga durasi - 1
                booked_dates.append(tanggal_sewa.strftime('%Y-%m-%d'))
                

    return render_template('add_pemesanan.html', id=id, merek=mobil.merek, harga_sewa=mobil.harga_sewa, denda_per_hari=mobil.denda_per_hari, nomor_plat=mobil.nomor_plat, booked_dates=booked_dates,
                          photo=mobil.photo )


from datetime import datetime

@pemesanan_blueprint.route('/pemesanan/<id>/save', methods=['POST'])
def save_pemesanan(id):
    if request.method == 'POST':
        mobil_id = id
        nama = request.form.get('nama')
        merek = request.form.get('merek')
        nomor_plat = request.form.get("nomor_plat")
        dateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_mobil = "dibooking" 
        
        try:
            denda_per_hari = int(request.form.get('denda_per_hari'))
        except ValueError:
            denda_per_hari = 0
        
        try:
            harga_sewa = int(request.form.get('harga_sewa'))
        except ValueError:
            harga_sewa = 0

        tgl_sewa = datetime.strptime(request.form['tgl_sewa'], '%Y-%m-%d').date()
        tgl_kembali = datetime.strptime(request.form['tgl_kembali'], '%Y-%m-%d').date()

        if tgl_sewa == tgl_kembali:  # Jika tanggal sewa dan tanggal kembali sama
            jumlah_hari = 1
        else:
            jumlah_hari = (tgl_kembali - tgl_sewa).days

        new_harga = (harga_sewa * jumlah_hari)

        # Melanjutkan logika lainnya...

        pemesanan = Pemesanan(mobil_id=mobil_id, nama=nama, merek=merek,
                              harga_sewa=harga_sewa, jumlah_hari=jumlah_hari,
                              tgl_sewa=tgl_sewa, tgl_kembali=tgl_kembali,
                              total_biaya=new_harga,
                              denda_per_hari=denda_per_hari, nomor_plat=nomor_plat, last_updated=dateNow,status_mobil=status_mobil)
        db.session.add(pemesanan)
        db.session.commit()



        # Lanjutkan dengan logika lainnya atau kembalikan respon yang sesuai


        if tgl_kembali < date.today(): # jika tanggal selesai sudah lewat
            pemesanan.status = 'selesai' # ubah status menjadi 'selesai'
            db.session.commit() # simpan perubahan ke database
            Pemesanan.query.filter_by(id=pemesanan.id).delete() # hapus pemesanan dari tabel
        flash(f"Anda telah memesan mobil ini: {merek} untuk {jumlah_hari} hari. Terima kasih, {nama}!")

        return redirect('/list_pesanan/1')
@pemesanan_blueprint.route('/booking/<id>/edit')
def edit_booking(id):
    booking = Pemesanan.query.filter_by(id=id).first()
    return render_template("edit_booking.html",booking=booking,id=id)

@pemesanan_blueprint.route('/bookingedit/<id>/save', methods=['POST'])
def save_editbooking(id):
        booking = Pemesanan.query.filter_by(id=id).first()
        nama = request.form.get('nama')
        merek = request.form.get('merek')
        nomor_plat = request.form.get("nomor_plat")
        dateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_mobil = request.form.get("status")
        
        try:
            denda_per_hari = int(request.form.get('denda_per_hari'))
        except ValueError:
            denda_per_hari = 0
        
        try:
            harga_sewa = int(request.form.get('harga_sewa'))
        except ValueError:
            harga_sewa = 0
        try:
            total_biaya = int(request.form.get('total_biaya'))
        except ValueError:
            total_biaya = 0
        try:
            jumlah_hari = int(request.form.get('jumlah_hari'))
        except ValueError:
            jumlah_hari = 0

        tgl_sewa = datetime.strptime(request.form['tgl_sewa'], '%Y-%m-%d').date()
        tgl_kembali = datetime.strptime(request.form['tgl_kembali'], '%Y-%m-%d').date()
        booking.nama=nama
        booking.merek=merek
        booking.nomor_plat=nomor_plat
        booking.last_updated=dateNow
        booking.denda_per_hari= denda_per_hari
        booking.jumlah_hari= jumlah_hari
        booking.harga_sewa=harga_sewa
        booking.total_biaya=total_biaya
        booking.tgl_sewa=tgl_sewa
        booking.tgl_kembali=tgl_kembali
        booking.status_mobil = status_mobil
        db.session.add(booking)
        db.session.commit()
        return redirect('/list_pesanan/1')

@pemesanan_blueprint.route('/add_transaksi2/<int:id>')
def add_transaksi2(id):
    

    # Dapatkan data pemesanan mobil yang sudah ada
    pemesanan = Pemesanan.query.filter_by(id=id).first()

    

    return render_template('add_booking.html', id=id,nama=pemesanan.nama, merek=pemesanan.merek, harga_sewa=pemesanan.harga_sewa, denda_per_hari=pemesanan.denda_per_hari, nomor_plat=pemesanan.nomor_plat, jumlah_hari=pemesanan.jumlah_hari,tgl_sewa=pemesanan.tgl_sewa,
                           tgl_kembali=pemesanan.tgl_kembali)



@pemesanan_blueprint.route('/transaksi2/<id>/save', methods=['POST'])
def sv_transaksi(id):
    if request.method == 'POST':
        pemesanan_id = id
        nama = request.form.get('nama')
        merek = request.form.get('merek')
        nomor_plat = request.form.get("nomor_plat")
        status = request.form.get("status")
        dateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_mobil = "dipinjam" 
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

        tgl_sewa = datetime.strptime(request.form['tgl_sewa'], '%Y-%m-%d').date()
        tgl_kembali = datetime.strptime(request.form['tgl_kembali'], '%Y-%m-%d').date()

        if tgl_sewa == tgl_kembali:  # Jika tanggal sewa dan tanggal kembali sama
            jumlah_hari = 1
        else:
            jumlah_hari = (tgl_kembali - tgl_sewa).days

        total_biaya = request.form.get('total_biaya')
        if total_biaya is not None:
           try:
            total_biaya = int(total_biaya)
           except ValueError:
            total_biaya = 0
        else:
           total_biaya = 0

        sisa_harga = request.form.get('sisa_harga')
        if sisa_harga is not None:
           try:
            sisa_harga = int(sisa_harga)
           except ValueError:
            sisa_harga = 0
        else:
         sisa_harga = 0


        new_harga = total_biaya + (harga_sewa * jumlah_hari)

        if dp > 0:
            sisa_harga = new_harga - dp
        else:
            sisa_harga = new_harga

        if dp >= new_harga:
            status = 'lunas'
        else:
            status = 'belum lunas'

        # Melanjutkan logika lainnya...

        pemesanan = MobilDisewa(pemesanan_id=pemesanan_id, nama=nama, merek=merek,
                              harga_sewa=harga_sewa, jumlah_hari=jumlah_hari,
                              tgl_sewa=tgl_sewa, tgl_kembali=tgl_kembali,
                              total_biaya=new_harga, status=status,
                              denda_per_hari=denda_per_hari, nomor_plat=nomor_plat, dp=dp, status_mobil=status_mobil, sisa_harga=sisa_harga,
                              last_updated=dateNow)
        db.session.add(pemesanan)
        db.session.commit()


        # Lanjutkan dengan logika lainnya atau kembalikan respon yang sesuai


        if tgl_kembali < date.today(): # jika tanggal selesai sudah lewat
            pemesanan.status = 'selesai' # ubah status menjadi 'selesai'
            db.session.commit() # simpan perubahan ke database
            MobilDisewa.query.filter_by(id=pemesanan.id).delete() # hapus pemesanan dari tabel
        flash(f"Anda telah memesan mobil ini: {merek} untuk {jumlah_hari} hari. Terima kasih, {nama}!")

        return redirect('/list_transaksikuy/1')
    
@pemesanan_blueprint.route('/pemesanan/<id>/edit')
def edit_pemesanan(id):
    obj = MobilDisewa.query.filter_by(id=id).first()
    return render_template("edit_pemesanan.html",obj=obj,id=id)


@pemesanan_blueprint.route('/editkuy/<id>/save',methods =['POST'])
def update_transaksi(id):
    obj = MobilDisewa.query.filter_by(id=id).first()
    f_nama = request.form.get("nama")
    f_merek = request.form.get("merek")
    f_no_plat = request.form.get("nomor_plat")
    dateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f_status = request.form.get("status")
    f_status_mobil = request.form.get("status_mobil")
    try:
            denda_per_hari = int(request.form.get('denda_per_hari'))
    except ValueError:
            denda_per_hari = 0
    try:
            sisa_harga = int(request.form.get('sisa_harga'))
    except ValueError:
            sisa_harga = 0
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

    tgl_sewa= datetime.strptime(request.form['tgl_sewa'], '%Y-%m-%d').date()  
    tgl_kembali = tgl_sewa + timedelta(days=int(jumlah_hari))
    try:
           total_biaya = int(request.form.get('total_biaya'))
    except ValueError:
           total_biaya = 0
          
    obj.nama=f_nama
    obj.merek=f_merek
    obj.nomor_plat=f_no_plat
    obj.denda_per_hari=denda_per_hari
    obj.harga_sewa=harga_sewa
    obj.jumlah_hari=jumlah_hari
    obj.tgl_sewa=tgl_sewa
    obj.tgl_kembali=tgl_kembali
    obj.sis_harga=sisa_harga
    obj.dp = dp
    obj.status = f_status
    obj.status_mobil = f_status_mobil
    obj.last_updated = dateNow
    obj.total_biaya = total_biaya

    db.session.add(obj)
    db.session.commit()
    return redirect('/list_transaksikuy/1')



@pemesanan_blueprint.route("/booking/<id>/delete")
def delete_jurnal(id):
    p = Pemesanan.query.filter_by(id=id).first()
    db.session.delete(p)
    db.session.commit()
    return redirect('/list_pesanan/1')

@pemesanan_blueprint.route("/pemesanan/<id>/delete")
def delete_mobildipinjam(id):
    mdp = MobilDisewa.query.filter_by(id=id).first()
    db.session.delete(mdp)
    db.session.commit()
    return redirect('/list_transaksikuy/1')
@pemesanan_blueprint.route("/booking/<int:id>/cancel")
def cancel_booking(id):
    # Mendapatkan data pemesanan berdasarkan ID
    pemesanan = Pemesanan.query.get(id)
    dateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if pemesanan is None:
        return 'Pemesanan tidak ditemukan', 404

    # Mengubah status pemesanan menjadi "Dibatalkan"
    pemesanan.status_mobil = 'Dibatalkan'
    pemesanan.last_updated = dateNow
    # Menyimpan perubahan ke database
    db.session.commit()
    return redirect('/list_pesanan/1')
    


# ...

@pemesanan_blueprint.route('/invoice/<int:id>')
def invoice(id):
    pemesanan = MobilDisewa.query.filter_by(id=id).first()

    # Data invoice
    invoice_data = {
        'id': pemesanan.id,
        'nama': pemesanan.nama,
        'merek': pemesanan.merek,
        'denda_per_hari': pemesanan.denda_per_hari,
        'jumlah_hari': pemesanan.jumlah_hari,
        'tgl_sewa': pemesanan.tgl_sewa,
        'tgl_kembali': pemesanan.tgl_kembali,
        'total_biaya': pemesanan.total_biaya,
        'status': pemesanan.status,
        'status_mobil': pemesanan.status_mobil
    }

    # Membuat PDF
    pdf = FPDF()
    pdf.add_page()

   
    # Menambahkan data pemesanan
    pdf.set_font("Arial", size=12)
    pdf.cell(50, 10, "Nama Pelanggan: ")
    pdf.cell(50, 10, invoice_data['nama'], 0, 1)
    pdf.cell(50, 10, "Merek Mobil: ")
    pdf.cell(50, 10, invoice_data['merek'], 0, 1)
    pdf.cell(50, 10, "Denda per Hari: ")
    pdf.cell(50, 10, str(invoice_data['denda_per_hari']), 0, 1)
    pdf.cell(50, 10, "Jumlah Hari: ")
    pdf.cell(50, 10, str(invoice_data['jumlah_hari']), 0, 1)
    pdf.cell(50, 10, "Tanggal Sewa: ")
    pdf.cell(50, 10, str(invoice_data['tgl_sewa']), 0, 1)
    pdf.cell(50, 10, "Tanggal Kembali: ")
    pdf.cell(50, 10, str(invoice_data['tgl_kembali']), 0, 1)
    pdf.cell(50, 10, "Total Biaya: ")
    pdf.cell(50, 10, str(invoice_data['total_biaya']), 0, 1)
    pdf.cell(50, 10, "Status: ")
    pdf.cell(50, 10, invoice_data['status'], 0, 1)
    pdf.cell(50, 10, "Status_mobil: ")
    pdf.cell(50, 10, invoice_data['status_mobil'], 0, 1)
    filename = "invoice_" + str(invoice_data['id']) + ".pdf"

    # Mendapatkan path absolut ke direktori invoices
    invoice_dir = os.path.join(os.getcwd(), 'invoices')

    # Mengecek apakah direktori invoices sudah ada, jika tidak, maka membuatnya
    if not os.path.exists(invoice_dir):
        os.makedirs(invoice_dir)

    # Menyimpan file PDF di direktori invoices
    pdf_path = os.path.join(invoice_dir, filename)
    pdf.output(pdf_path)

    return send_from_directory(invoice_dir, filename, as_attachment=True)

@pemesanan_blueprint.route('/add_booking/<int:id>')
def add_booking(id):
    mobil = Mobil.query.get(id)

   
  

    return render_template('add_booking.html', id=id, merek=mobil.merek, harga_sewa=mobil.harga_sewa, denda_per_hari=mobil.denda_per_hari)

from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import AnnotationBuilder
from flask import send_from_directory
import pdfkit



from io import BytesIO

@pemesanan_blueprint.route('/invoicekuy/<int:id>')
def invoicekuy(id):
    pemesanan = MobilDisewa.query.filter_by(id=id).first()
    m = Pemesanan.query.filter_by(id=pemesanan.pemesanan_id).first()
    dateNow = date.today()

    invoice_data = {
        'id': pemesanan.id,
        'nama': pemesanan.nama,
        'merek': pemesanan.merek,
        'denda_per_hari': pemesanan.denda_per_hari,
        'jumlah_hari': pemesanan.jumlah_hari,
        'tgl_sewa': pemesanan.tgl_sewa,
        'tgl_kembali': pemesanan.tgl_kembali,
        'total_biaya': pemesanan.total_biaya,
        'status': pemesanan.status,
        'status_mobil': pemesanan.status_mobil,
        'date': dateNow,
        'nomorPolisi': m.nomor_plat,
        'merk': m.merek
    }

    rendered_template = render_template('invoice_template.html', data=invoice_data)

    # Konversi HTML menjadi PDF dalam bentuk byte array
    pdf_bytes = pdfkit.from_string(rendered_template, False, configuration=config)

    # Simpan file PDF pada direktori temporary
    pdf_file_path = f'invoices/invoice_{pemesanan.id}.pdf'
    with open(pdf_file_path, 'wb') as file:
        file.write(pdf_bytes)

    return send_file(pdf_file_path, as_attachment=True)
