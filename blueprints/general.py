from flask import Blueprint

bp = Blueprint("general" , __name__)

@bp.route("/")
def main() :
    return "this is main page"


@bp.route("/about")
def about() :
    return "About Us"