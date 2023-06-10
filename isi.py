from flask import Blueprint ,render_template,request,  redirect
from mobil_model import User, db

from app import* 
from datetime import datetime
from werkzeug.security import generate_password_hash
app.app_context().push()

user = User()
user.username = 'nebula'
user.password = generate_password_hash('goreng',method='sha256')


db.session.add_all([user])
db.session.commit()