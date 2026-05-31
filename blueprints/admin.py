from flask import Blueprint,render_template,request,session,redirect,abort,url_for
from config import ADMIN_USERNAME,ADMIN_PASSWORD
from extentions import db
from models.tables import Product

bp = Blueprint("admin" , __name__)


@bp.before_request
def before_request() :
    if session.get("admin_login") is None and request.endpoint != "admin.login" :
        abort(403)


@bp.route("/admin/login" , methods= ["POST" , "GET"])
def login() :
    username = request.form.get("username", None)
    password = request.form.get("password", None)

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD :
        session["admin_login"] = username
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/login.html')


@bp.route("/admin/dashboard" , methods= ["POST","GET"])
def dashboard() :
    if session.get("admin_login") is None:
        abort(403)
    
    return render_template('admin/dashboard.html')


@bp.route("/admin/dashboard/product" , methods= ["POST","GET"])
def product() :

    if request.method == "GET" :
        products = Product.query.all()
        return render_template('admin/product.html' , products=products)

    name = request.form.get("name")
    description = request.form.get("description")
    price = request.form.get("price")
    active = request.form.get("active")

    p = Product(name=name , description=description , price=price)
    if active == None :
        p.active = 0
    else :
        p.active = 1

    db.session.add(p)
    db.session.commit()
    
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

        product.name = name
        product.description = description
        product.price = price
        if active == None :
            product.active = 0
        else :
            product.active = 1

        db.session.commit()

        return redirect(url_for("admin.product"))

    

