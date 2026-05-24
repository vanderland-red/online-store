from flask import Blueprint

bp = Blueprint("admin" , __name__)

@bp.route("/admin")
def admin() :
    return 'this is admin page'