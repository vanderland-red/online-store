from flask import Blueprint

bp = Blueprint("user" , __name__)

@bp.route("/admin")
def user() :
    return 'this is user page'