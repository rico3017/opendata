import os, sys, platform
from gevent import monkey
from flask import Flask, session, g, render_template
from model.database import *

monkey.patch_all()

basedir = os.path.dirname(os.path.abspath(__file__)) 
sys.path.insert(0,basedir)

from views import hsePrRec, londonMap

app = Flask(__name__)
app.register_blueprint(hsePrRec.mod)
app.register_blueprint(londonMap.mod)



@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.teardown_request
def remove_db_session(exception):
    db_session.remove()


if __name__ == "__main__":
    if "Windows" in platform.platform():
        app.debug = True
    app.config["JSON_AS_ASCII"] = False
    app.run(host = "0.0.0.0")
    #databaseTest()