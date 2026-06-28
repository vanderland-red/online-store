from flask import Blueprint,render_template,url_for,request
from models.tables import Product
from sqlalchemy import func

bp = Blueprint("general" , __name__)

@bp.route("/")
def main() :
    search = request.args.get("search", "").strip()

    if search:
        product = Product.query.filter(
            Product.active == 1,
            Product.name.ilike(f"%{search}%")
        ).all()
    else:
        product = Product.query.filter(Product.active == 1).order_by(func.random()).all()

        
    return render_template("main.html" , product=product, search=search)


@bp.route("/product/<int:id>/<name>")
def product(id, name): # وقتی کاربر کلیک کرد روی محصول براش این داده ها ارسا بشه
    product = Product.query.filter(
        Product.id == id, 
        Product.name == name,
        Product.active == 1
    ).first_or_404()

    # پیدا کردن محصولات مشابه
    list_product_name = Product.query.filter(Product.name == name).first()
    base_name = list_product_name.name[:5]

    another_product = Product.query.filter(
        Product.active == 1,
        Product.id != list_product_name.id,
        Product.name.ilike(f'%{base_name}%')
        ).order_by(func.random()).limit(3).all()

    return render_template('product_this.html', product=product, another_product=another_product)

    

@bp.route("/about")
def about() :
    return render_template('about.html')