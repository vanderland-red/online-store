from flask import Flask
from blueprints.general import bp as general
from blueprints.user import bp as user
from blueprints.admin import bp as admin
from config import SQLALCHEMY_DATABASE_URI
from extentions import db
from models.users import User , Product

app = Flask(__name__)

app.register_blueprint(general)
app.register_blueprint(user)
app.register_blueprint(admin)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.db = db
_ = User, Product


if __name__ == "__main__":
    app.run(debug=True)