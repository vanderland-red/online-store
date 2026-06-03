from flask import Blueprint, render_template, request, redirect, url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required
from models.tables import User
from extentions import db

bp = Blueprint("user", __name__)

@bp.route("/user/dashboard")
@login_required
def dashboard_user():
    return render_template("user/dashboard_user.html")

@bp.route("/user/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template('user/login_user.html')
    
    username = request.form.get("username")
    password = request.form.get("password")
    phone = request.form.get("phone")
    address = request.form.get("address")
    
    if not username or not password:
        return "نام کاربری و رمز عبور الزامی است"
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return "این نام کاربری قبلاً ثبت شده است"
    
    u = User(
        username=username,
        password=generate_password_hash(password),
        phone=phone,
        address=address
    )
    
    db.session.add(u)
    db.session.commit()
    
    flash("ثبت نام با موفقیت انجام شد")
    return redirect(url_for('user.register'))

@bp.route("/user/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template('user/login_user.html')
    
    username = request.form.get("username")
    password = request.form.get("password")
    
    if not username or not password:
        return "نام کاربری و رمز عبور الزامی است"
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        return "نام کاربری یا رمز عبور اشتباه است"
    
    login_user(user)
    
    return redirect(url_for('user.dashboard_user'))
