import os
from flask import Flask
from views import pages
from conf_basic import app_config

app = Flask(__name__)
app.register_blueprint(pages) 

if __name__ == "__main__":
    app.run(host=app_config['host_name'],port = app_config['port'],debug = app_config['debug'])

