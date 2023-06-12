import os
from flask import Flask, Blueprint, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.mobil_model import User, db

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rental.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.Session.get(int(user_id))

login_blueprint = Blueprint("login_blueprint", __name__)

@login_blueprint.route("/login/", methods=["GET"])
def login():
    return render_template("login2.html")
@login_blueprint.route("/loginkuy/", methods=["GET"])
def loginkuy():
    return render_template("loginkuy.html")


@login_blueprint.route('/login/save', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login_blueprint.login'))
    login_user(user)
    return redirect(f'/sewa')

@login_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(f'/login/')

@login_blueprint.route('/signup')
def signup_menu():
    return render_template('signup.html')


@login_blueprint.route('/signup/save', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Ambil data dari form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validasi data
        if password != confirm_password:
            flash('Password tidak cocok')
            return redirect('/signup')
        elif User.query.filter_by(username=username).first():
            flash('Username sudah digunakan')
            return redirect('/signup')
        elif User.query.filter_by(email=email).first():
            flash('Email sudah digunakan')
            return redirect('/signup')
        else:
            # Hash password
            hashed_password = generate_password_hash(password)

            # Simpan data ke database
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Akun berhasil dibuat')
            return redirect(f'/sewa')
    return render_template('signup.html')


app.register_blueprint(login_blueprint)

