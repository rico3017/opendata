from flask import Blueprint,jsonify,request,abort
from model.database import myDbConPool
from random import randint


mod = Blueprint("swagger", __name__, url_prefix="/swagger")


@mod.route("/test/", methods = ["POST", "GET"])
def concurrent():
    """Example endpoint returning a list of colors by palette
    This is using docstrings for specifications.
    ---
    parameters:
      - name: rico
        in: query
        type: string
        enum: ['1']
        required: true
    definitions:
      rico:
        type: string
    responses:
      200:
        description: a list of books
        schema:
          $ref: '#/definitions/rico'
        examples:
          rico: ['1','2']
    """
    if "rico" in request.values:
        page = 20
        offset = randint(0, 245316)
        start = page * offset
        end = start + page
        conn = myDbConPool.connect()
        cursor = conn.cursor()
        cursor.execute("select * from test_data where id between %d and %d" % (start, end))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(msg = "success", start = start ,result = result)
    else:
        abort(403)


