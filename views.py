from flask import Blueprint, render_template,redirect, abort,request
from jinja2 import TemplateNotFound

pages = Blueprint('pages', __name__)

@pages.route("/")
def start():
    return render_template("welcome.html")

@pages.route("/home")
def index():
    #show_index()
    return render_template("index.html",title = "This is the index page")
@pages.route("/login")
def login():
    return render_template("login.html")
