from flask import Flask
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from extentions import db
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_migrate import Migrate

from blueprints.general import bp as general
from blueprints.user import bp as user
from blueprints.admin import bp as admin

from models.tables import User, Product, Cart, CartItem, Payment


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = SECRET_KEY

csrf = CSRFProtect(app)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = "user.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(general)
app.register_blueprint(user)
app.register_blueprint(admin)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
