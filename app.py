
import os,pdfkit,jinja2
from flask import Flask, render_template, request, redirect, url_for,flash
from blueprint import mobil_blueprint,detail_mobil_blueprint, pemesanan_blueprint,login_blueprint,transaksi_blueprint
from extensions import *
from models import User

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user




app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental.db'
app.config['UPLOAD_FOLDER'] = os.path.abspath(os.path.dirname(__file__)) + "\static\media/"
path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
ALLOWED_EXTENSIONS = { 'pdf', 'png', 'jpg', 'jpeg'}

db.init_app(app)
migrate.init_app(app, db=db)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



app.register_blueprint(mobil_blueprint)
app.register_blueprint(detail_mobil_blueprint)
app.register_blueprint(pemesanan_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(transaksi_blueprint)

login_manager.init_app(app)

if "__main__" ==__name__:
     app.run(debug= True,port =4000)
