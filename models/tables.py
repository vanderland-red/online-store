from flask_login import UserMixin
from extentions import db,get_current_time


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=True, index=True)
    address = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"







class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, index=True)
    active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<Product {self.name}>"







class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False
    )

    user = db.relationship("User", backref="carts")


    def total_price(self):
        total = 0
        for item in self.cart_items:
            total += item.product.price * item.quantity
        return total
    

    def get_status_persian(self):
        if self.status == 'pending':
            return 'در انتظار پرداخت (سبد خرید)'
        
        if self.status == 'paid':
            return 'پرداخت شده'
        
        if self.status == 'sent':
            return 'ارسال شده'
        
        if self.status == 'rejected':
            return 'رد شده'
        

    def __repr__(self):
        return f"<Cart id={self.id} status={self.status}>"








class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.String(15), default= get_current_time)
    token = db.Column(db.String(255))
    refid = db.Column(db.String(255)) #شماره پیگیری تراکنش   
    transation_id = db.Column(db.String(255)) #پیگیری تراکنش
    card_pan = db.Column(db.String(255)) #نمایشی از ارقام کارت 

    cart_id = db.Column(
        db.Integer,
        db.ForeignKey('carts.id'),
        nullable=False
    )
    cart = db.relationship("Cart", backref="payments")

    def get_status_persian(self):
        if self.status in ["pending"]:
            return "در انتظار پرداخت..."

        if self.status in ["success", "paid"]:
            return "پرداخت شده✅"

        if self.status in ["failed", "rejected"]:
            return "عدم پرداخت❌"

        return "نامشخص"

    def __repr__(self):
        return f"<Payment id={self.id} status={self.status}>"
    






class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


    product = db.relationship("Product", backref="cart_items")
    cart = db.relationship("Cart", backref="cart_items")




class UserSuggestion(db.Model):
    __tablename__ = 'user_suggestions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    suggestion_text = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())