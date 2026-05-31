from flask import Blueprint,render_template,url_for
from models.tables import Product

bp = Blueprint("general" , __name__)

@bp.route("/")
def main() :
    product = Product.query.filter(Product.active == 1).all()
    return render_template("main.html" , product=product)


@bp.route("/product/<int:id>/<name>")
def product(id, name):
    product = Product.query.filter(
        Product.id == id, 
        Product.name == name,
        Product.active == 1
    ).first_or_404()
    return render_template('product_this.html', product=product)

@bp.route("/about")
def about() :
    return render_template('about.html')