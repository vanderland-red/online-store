from flask import Blueprint

app = Blueprint("user" , __name__)

@app.route("/admin")
def user() :
    return 'this is user page'