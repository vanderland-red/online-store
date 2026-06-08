from flask import Blueprint,render_template,request,session,redirect,abort,url_for
from config import ADMIN_USERNAME,ADMIN_PASSWORD
from extentions import db
from models.tables import Product,Cart

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
    carts = Cart.query.filter(Cart.status != 'pending').all()

    return render_template('admin/dashboard.html', carts=carts)


@bp.route("/admin/dashboard/order/<id>" , methods= ["POST","GET"])
def order(id) :
    cart = Cart.query.filter(Cart.id == id).first_or_404()

    if request.method == "GET":
         return render_template('admin/order.html', cart=cart)
    
    else :
        status = request.form.get("status")
        cart.status = status
        db.session.commit()
        return redirect(url_for('admin.order', id=id))
   


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


    

