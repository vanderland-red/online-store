from flask import Blueprint, render_template, request, redirect, url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required,current_user,logout_user
from models.tables import User,Cart,Product,CartItem,Payment,UserSuggestion
from extentions import db
import uuid
import re

bp = Blueprint("user", __name__)


@bp.route("/user/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template('user/login_user.html')
    
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    phone = request.form.get("phone", "").strip()
    address = request.form.get("address")
    
    if not username or not password:
        flash("رمز عبور را وارد نمایید", "error")
        return redirect(url_for("user.register"))
    
    if len(username) < 7 :
        flash(" نام کاربری باید بیشتر از 7 کلمه باشد", "error")
        return redirect(url_for("user.register"))
    
    if len(password) < 5 :
        flash("رمز عبور ایمن نیست", "error")
        return redirect(url_for("user.register"))
    
    if not re.fullmatch(r"(?:\+98|0)9\d{9}", phone):
        flash("شماره موبایل وارد شده صحیح نیست", "info")
        return redirect(url_for("user.register"))
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash("این نام کاربری قبلا انتخاب شده است", "warning")
        return redirect(url_for("user.register"))
    
    u = User(
        username=username,
        password=generate_password_hash(password),
        phone=phone,
        address=address
    )

    db.session.add(u)
    db.session.commit()

    login_user(u)
    
    flash("ثبت نام با موفقیت انجام شد", "success")
    return redirect(url_for('general.main'))



@bp.route("/user/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated :
            return redirect(url_for("user.dashboard_user"))
        return render_template('user/login_user.html')
    
    username = request.form.get("username")
    password = request.form.get("password")
    
    if not username or not password:
        flash("رمز عبور یا نام کاربری اشتباه است", "error")
        return redirect(url_for("user.login"))
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        flash("رمز عبور یا نام کاربری اشتباه است", "error")
        return redirect(url_for("user.login"))
    
    login_user(user)
    flash(" با موفقیت وارد شدید", "success")
    return redirect(url_for('user.dashboard_user'))



@bp.route("/cart", methods = ["GET"])
@login_required
def cart():
    return render_template("user/cart.html")


@bp.route("/add-to-cart", methods=["GET"])
def add_to_cart():
    if not current_user.is_authenticated:
        flash("برای اضافه کردن محصول به سبد خرید، ابتدا وارد حساب کاربری شوید", "error")
        return redirect(url_for("user.login"))

    id = request.args.get("id")
    product = Product.query.filter(Product.id == id).first_or_404()

    cart = Cart.query.filter_by(user_id=current_user.id, status="pending").first()
    if cart is None:
        cart = Cart(status="pending", user=current_user)
        db.session.add(cart)
        db.session.commit()

    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product.id
    ).first()

    if cart_item is None:
        item = CartItem(quantity=1, cart=cart, product=product)
        item.price = product.price
        db.session.add(item)
    else:
        cart_item.quantity += 1

    db.session.commit()

    flash("محصول با موفقیت به سبد خرید اضافه شد", "success")
    return redirect(url_for("user.cart"))

@bp.route("/dashboard", methods=["GET"])
@login_required
def cart_empty():
    cart = Cart.query.filter_by(
        user_id=current_user.id,
        status="pending"
    ).first()

    return render_template("user/dashboard_user.html", cart=cart)



@bp.route("/remove-from-cart/<int:item_id>", methods=["GET"])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query \
        .join(Cart) \
        .filter(
            CartItem.id == item_id,
            Cart.user_id == current_user.id,
            Cart.status == "pending"
        ).first_or_404()
    
    if cart_item.quantity > 1 :
        cart_item.quantity -= 1
    else :
        db.session.delete(cart_item)

    db.session.commit()

    remaining_items = CartItem.query.filter_by(cart_id=cart_item.cart_id).count()
    if remaining_items == 0:
        flash("سبد خرید خالی شد", "info")

    flash("محصول از سبد خرید حذف شد", "success")
    return redirect(url_for("user.cart"))


@bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("با موفقیت از حساب کاربری خارج شدید", "success")
    return redirect(url_for("user.register"))







@bp.route("/payment", methods=["POST"])
@login_required
def payment():

    cart = Cart.query.filter_by(
        user_id=current_user.id,
        status="pending"
    ).first()

    if not cart:
        return "سبد خریدی برای پرداخت وجود ندارد", 400

    token = str(uuid.uuid4())

    pay = Payment(
        token=token,
        price=cart.total_price(),
        status="pending",
        cart=cart
    )

    db.session.add(pay)
    db.session.commit()

    return redirect(url_for("user.mock_gateway", token=token))


@bp.route("/mock-gateway/<token>", methods=["GET"])
@login_required
def mock_gateway(token):

    payment = Payment.query.filter_by(token=token).first_or_404()

    return render_template("user/mock_gateway.html", payment=payment)



@bp.route("/verify", methods=["POST"])
@login_required
def verify():

    token = request.form.get("token")
    result = request.form.get("result")

    payment = Payment.query.filter_by(token=token).first_or_404()

    if result == "success":
        payment.status = "paid"
        payment.cart.status = "paid"
        payment.refid = "refid"
        payment.transation_id = "transation_id"
        payment.card_pan = "card_pan"
        flash("پرداخت با موفقیت انجام شد ", "success")
    else:
        payment.status = "failed"
        flash("پرداخت ناموفق بود ", "error")

    db.session.commit()

    return redirect(url_for("user.dashboard_user"))


@bp.route("/user/dashboard")
@login_required
def dashboard_user():
    cart = Cart.query.filter_by(
        user_id=current_user.id
    ).first()
    return render_template("user/dashboard_user.html", cart=cart)



@bp.route("/user/dashboard", methods=["GET", "POST"])
@login_required
def dashboard_user_change():

    if request.method == "GET":
        return render_template("user/dashboard_user.html")

    username = request.form.get("username")
    password = request.form.get("password")
    phone = request.form.get("phone")
    address = request.form.get("address")

    if not username:
        flash("نام کاربری را وارد نمایید", "error")
        return redirect(url_for("user.dashboard_user_change"))

    existing_user = User.query.filter(
        User.username == username,
        User.id != current_user.id
    ).first()

    if existing_user:
        flash("این نام کاربری قبلا انتخاب شده است", "warning")
        return redirect(url_for("user.dashboard_user_change"))

    current_user.username = username

    if password:
        current_user.password = generate_password_hash(password)

    current_user.phone = phone
    current_user.address = address

    db.session.commit()

    flash("اطلاعات با موفقیت بروزرسانی شد", "success")
    return redirect(url_for("user.dashboard_user_change"))


@bp.route("/user/dashboard/order/<id>", methods=["GET"])
@login_required
def order(id):
    cart = Cart.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return render_template("user/order_user.html", cart=cart)


@bp.route("/user/dashboard/suggestion", methods=["POST"])
@login_required
def suggestion() :

    suggestion_text = request.form.get("suggestion", "").strip()

    if suggestion_text == "" :
        flash("لطفا متن پیشنهاد را وارد کنید", "info")
        return redirect(url_for("user.dashboard_user"))
    
    add = UserSuggestion(
        user_id = current_user.id,
        suggestion_text=suggestion_text
        )
    db.session.add(add)
    db.session.commit()
    flash("پیشنهاد شما با موفقیت ارسال شد", "success")
    return redirect(url_for("user.dashboard_user"))