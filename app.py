import os
from flask import Flask, Blueprint, render_template,redirect, abort, request, session, flash
from jinja2 import TemplateNotFound
from conf_basic import app_config

from Object.User import User

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASEROOT = app.root_path + app_config['DataBaseRoot'],
    LOGIN = app_config['Login']
))


user = User(app.config['DATABASEROOT']+app.config['LOGIN'])
#app.register_blueprint(app) 


#app = Blueprint('app', __name__)

# Error message for invaild login
LOGIN_USER_PASS_ERROR = "Username or Password are not mathch to our record"
SIGN_UP_PASSWORD_NOT_MATCH = "The password you enter does not match"
SIGN_UP_USERNAME_TAKEN = "The username you enter has been used"


@app.route("/")
def start():
    return render_template("welcome.html")

@app.route("/home")
def index():
    #show_index()
    return render_template("home.html",title = "Index")

@app.route("/login", methods=['GET', 'POST'])
def login():
    page = request.args.get("page",None)
    if page is None:
        return login_(request)

    if page == "signup":
        return redirect("/signup")
    elif page== 'success':
        if user.islogin():
            return render_template("login_success.html",username = user.getusername())
        else:
            return redirect("/login")
    else:
        return redirect("/login") 

    #should never get to here
    abort(404)

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    error = []
    if request.method == 'POST':
        if request.form['password'] != request.form['repassword']:
            error.append(SIGN_UP_PASSWORD_NOT_MATCH)
        else:    
            if user.signup(request.form['username'],request.form['password']):
                return render_template("login_success.html",username = user.getusername())
            else:
                errpr.append(SIGN_UP_USERNAME_TAKEN)
    return render_template("signup.html",error = error) 

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.errorhandler(404)
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
        if user.login(request.form['username'],request.form['password']):
            return redirect ("/login?page=success")
        else:    
            error = LOGIN_USER_PASS_ERROR
    return render_template("login.html",error=error)


if __name__ == "__main__":
    app.run(host=app_config['host_name'],port = app_config['port'],debug = app_config['debug'])


