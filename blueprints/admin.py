from flask import Blueprint,render_template,request,session,redirect,abort,url_for,flash
from config import ADMIN_USERNAME,ADMIN_PASSWORD
from extentions import db
from models.tables import Product,Cart

bp = Blueprint("admin" , __name__)


@bp.before_request
def before_request() :
    if session.get("admin_login") is None and request.endpoint != "admin.login" :
        abort(403)


@bp.route("/admin/login", methods=["GET", "POST"])
def login():

    # اگر قبلاً لاگین کرده، دیگه صفحه لاگین نشون نمیده
    if session.get("admin_login"):
        return redirect(url_for("admin.dashboard"))

    if request.method == "GET":
        return render_template("admin/login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
        flash("نام کاربری یا رمز عبور اشتباه است", "error")
        return render_template("admin/login.html")

    # ذخیره وضعیت لاگین
    session["admin_login"] = username
    flash("با موفقیت وارد شدید", "success")
    return redirect(url_for("admin.dashboard"))


@bp.route("/admin/logout")
def logout():
    session.pop("admin_login", None)  # حذف لاگین ادمین
    flash("با موفقیت از پنل مدیریت خارج شدید", "success")
    return redirect(url_for("admin.login"))

@bp.route("/admin/dashboard" , methods= ["POST","GET"])
def dashboard() :
    if session.get("admin_login") is None:
        abort(403)
    carts = Cart.query.filter(Cart.status != 'pending').all()

    return render_template('admin/dashboard.html', carts=carts)


@bp.route("/admin/dashboard/order/<int:id>", methods=["GET", "POST"])
def order(id):
    cart = Cart.query.get_or_404(id)

    if request.method == "POST":
        status = request.form.get("status")

        if status in ["pending", "paid", "sent", "rejected"]:
            cart.status = status
            db.session.commit()

        return redirect(url_for("admin.order", id=id))

    return render_template("admin/order.html", cart=cart)
   


@bp.route("/admin/dashboard/product" , methods= ["POST","GET"])
def product() :

    if request.method == "GET" :
        product = Product.query.all()
        return render_template('admin/product.html' , products=product)

    name = request.form.get("name")
    description = request.form.get("description")
    price = request.form.get("price")
    active = request.form.get("active")
    file = request.files.get("cover")

    p = Product(name=name , description=description , price=price)
    if active == None :
        p.active = 0
    else :
        p.active = 1

    db.session.add(p)
    db.session.commit()

    file.save(f'static/cover/{p.id}.jpg')
    
    return 'Oh Yeh Man!!'


@bp.route("/admin/dashboard/edit_product/<id>" , methods= ["POST","GET"])
def edit_product(id) :
    product = Product.query.get_or_404(id)

    if request.method == "GET" :
        return render_template("admin/edit_product.html" , product=product)

    else :
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        active = request.form.get("active")
        file = request.files.get("cover")

        product.name = name
        product.description = description
        product.price = price
        if active == None :
            product.active = 0
        else :
            product.active = 1

        db.session.commit()

        if file and file.filename != '':
            file.save(f'static/cover/{ product.id }.jpg')

        return redirect(url_for("admin.product"))


    

