import os, sys, platform
from gevent import monkey
from flask import Flask, session, g, render_template, request, send_from_directory
from model.database import *

monkey.patch_all()

basedir = os.path.dirname(os.path.abspath(__file__)) 
sys.path.insert(0,basedir)

from views import hsePrRec, londonMap

app = Flask(__name__, static_url_path='')
app.register_blueprint(hsePrRec.mod)
app.register_blueprint(londonMap.mod)

@app.route('/home')
def www():
    return render_template('htdocs/index.html'), 200

@app.route('/location')
def location():
		
    return render_template('htdocs/location.html'), 200

@app.route('/constructing')
def constructing():
    return render_template('htdocs/construction.html'), 200

@app.route('/assets/<path:path>')
def asserts(path):
    return send_from_directory('templates/htdocs/assets', path)
    
@app.route('/commons/<path:path>')
def commons(path):
    return send_from_directory('templates/htdocs/commons', path)
    
@app.route('/imgs/<path:path>')
def imgs(path):
    return send_from_directory('templates/htdocs/imgs', path)


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
    app.run(host = "0.0.0.0", port=5000)