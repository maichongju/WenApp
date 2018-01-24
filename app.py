import os
from flask import Flask, Blueprint, render_template,redirect, abort, request, session, flash
from jinja2 import TemplateNotFound
from conf_basic import app_config, database_config

from Object.User import User
from Object.Blog import Blogs
from Object.DataBase import DataBase

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DATABASEROOT = app.root_path + app_config['DataBaseRoot'],
    LOGIN = app_config['Login']
))

db = DataBase(app.root_path + "\config.ini")
user = User(db)
blogs = Blogs(db)

#app.register_blueprint(app)


#app = Blueprint('app', __name__)

# Error message for invalid login
LOGIN_USER_PASS_ERROR = "User name or Password are not match to our record"
SERVER_UNVALIABLE = "Server Out Of Server"
SIGN_UP_PASSWORD_NOT_MATCH = "The password you enter does not match"
SIGN_UP_USERNAME_TAKEN = "The user name you enter has been used"
PROFILE_PASSWORD_NOT_MATCH = "The password you enter does not match"
PROFILE_PASSWORD_OLD_NOT_MATHC = "The old password not correct"


@app.route("/")
def start():
    return render_template("welcome.html")

@app.route("/home")
def index():
    #show_index()
    return render_template("home.html",user = user)

@app.route("/myprofile", methods=['GET','POST'])
def profile():
    if not user.islogin():
        abort(401)
    page = request.args.get("page",None)
    if page == "changepassword":
        return changepassword(request)
    elif page == "other":
        return othertab(request)

    return render_template("profile.html", user = user, error= None ,section = None)

def changepassword(request):
    """
    Function will check the old password with the database and
    check if the new password match, then it will update the data
    in the database
    """
    section = 'password'
    error = []
    if request.form['new_pas'] != request.form['re_pas']:
        error.append(PROFILE_PASSWORD_NOT_MATCH)
        return render_template("profile.html",user = user, error = error, section = section)
    else:
        result = user.update_password(request.form['old_pas'],request.form['new_pas'])
        if not result:
            error.append(PROFILE_PASSWORD_OLD_NOT_MATHC)
            return render_template("profile.html",user = user, error = error, section = section)
    return render_template("profile.html",user = user, error = None ,section = section)

def othertab(request):
    """
    Function will deal with the request from other tab
    """
    section = 'other'
    if "logout" in request.form:
        return logout()
    elif "del_acc" in request.form:
        return delete()
    return render_template("profile.html", user = user, error = None, section = section)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if user.islogin():
        redirect("/home")
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
    elif page == 'logout':
        return logout()
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
            return render_template("signup.html",error = error)
        else:
            if user.signup(request.form['username'],request.form['password']):
                if user.islogin():
                    return redirect("/home")
                else:
                    return render_template("login_success.html",username = user.getusername())
            else:
                error.append(SIGN_UP_USERNAME_TAKEN)
                return render_template("signup.html",error = error)
    error = None
    return render_template("signup.html",error = error)

@app.route("/blog")
def blog():
    ID = request.args.get("ID",None)
    if ID is None:
        return render_template("blog.html",user = user,blogs = blogs.getblogs())
    else:
        return getoneblog(ID)

def getoneblog(Id):
    """
    Helper funtion for blog, get a single blog
    """
    blog = blogs.getblog(Id)
    if blog is None:
        abort(404)
    else:
        return render_template("blog_template.html",user = user, blog = blog)

@app.route("/editblog")
def editblog():
    return render_template("edit_blog.html",user = user)

@app.route("/about")
def about():
    return render_template("about.html",user = user)

@app.errorhandler(404)
def handle_error(e):
    return render_template("error404.html", user = user), 404

@app.errorhandler(401)
def error401(e):
    return render_template("error401.html",user = user),401

def login_(request):
    """
    helper function for login
    postcondition:
        request : request object from the login page
    """
    if request.method == 'POST':
        result,error = user.login(request.form['username'],request.form['password'])
        if result:
            return redirect ("/login?page=success")
    return render_template("login.html",error=error)

def logout():
    """
    Function will logout current user
    """
    user.logout()
    return redirect("/home")

def delete():
    """
    Function will delete current user
    """
    user.delete_account()
    return redirect("/home")


if __name__ == "__main__":
    app.run(host=app_config['host_name'],port = app_config['port'],debug = app_config['debug'])
