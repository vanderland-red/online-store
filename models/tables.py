from flask_login import UserMixin
from extentions import db


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

    def __repr__(self):
        return f"<Cart id={self.id} status={self.status}>"


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False)

    cart_id = db.Column(
        db.Integer,
        db.ForeignKey('carts.id'),
        nullable=False
    )
    cart = db.relationship("Cart", backref="payments")

    def __repr__(self):
        return f"<Payment id={self.id} status={self.status}>"