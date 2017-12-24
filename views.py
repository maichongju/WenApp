from app import app
from flask import Blueprint, render_template,redirect, abort, request, session, flash
from jinja2 import TemplateNotFound

pages = Blueprint('pages', __name__)

# Error message for invaild login
LOGIN_USER_PASS_ERROR = "Username or Password are not mathch to our record"
SIGN_UP_PASSWORD_NOT_MATCH = "The password you enter does not match"
SIGN_UP_USERNAME_TAKEN = "The username you enter has been used"


@pages.route("/")
def start():
    return render_template("welcome.html")

@pages.route("/home")
def index():
    #show_index()
    return render_template("home.html",title = "Index")

@pages.route("/login", methods=['GET', 'POST'])
def login():
    page = request.args.get("page",None)
    if page is None:
        return login_(request)

    if page == "signup":
        return redirect("/signup")
    else:
        return redirect("/login") 

    #should never get to here
    abort(404)

@pages.route("/signup", methods = ['GET', 'POST'])
def signup():
    error = []
    print("signup")
    if request.method == 'POST':
        if request.form['password'] != request.form['repassword']:
            error.append(SIGN_UP_PASSWORD_NOT_MATCH)
            error.append(SIGN_UP_USERNAME_TAKEN)
        if len(error) == 0:
            error = None
    return render_template("signup.html",error = error) 

@pages.route("/gallery")
def gallery():
    return render_template("gallery.html")

@pages.route("/about")
def about():
    return render_template("about.html")

@pages.errorhandler(404)
def handle_error(e):
    
    return render_template("error404.html"), 404

def login_(request):
    """
    helper function for login
    postcondition:
        request : request object from the login page
    """
    error = None
    if request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])
    return render_template("login.html",error=error)
