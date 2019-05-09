from flask import Blueprint, jsonify, request,abort
from myconfig import page_size, apis
from myutil.mylog import mylog
import requests, datetime, json, traceback


mod = Blueprint("house", __name__, url_prefix="/house")


@mod.route("/price/", methods = ["POST", "GET"])
def price():
    try:
        results = []
        if "postcode" not in request.values and "street" not in request.values:
            abort(416)
        params = {}
        params["_pageSize"] = page_size
        params["propertyAddress.town"] = "LONDON"
        params["_sort"] = "-transactionDate"
        if "page" in request.values:
            params["_page"] = request.values["page"]
        else:
            params["_page"]  = 0
        if "postcode" in request.values and len(request.values["postcode"]):
            params["propertyAddress.postcode"] = request.values["postcode"].upper()
        if "street" in request.values and len(request.values["street"]):
            params["propertyAddress.street"] = request.values["street"].upper()
            '''
            now = datetime.datetime.now()
            year = datetime.timedelta(days=365)
            year = year * 3
            start_date = now - year
            start = start_date.strftime("%Y-%m-%d") 
            params["min-transactionDate"] = start
            ''' 
        mylog(msg = "/house/price:" + json.dumps(params), file = "send.log", handler = 0b10)
        res = requests.get(apis["property_url"], params = params)
        mylog(msg = "/house/price:" + str(res.content), file = "receive.log", handler = 0b10)
        if res.status_code == 200:
            dic = res.json()
            items = dic["result"]["items"]
            if len(items) > 0:
                msg = "success"
            elif params["_page"] == 0:
                msg = "No results!"
            else:
                msg = "No more data!"
            for item in items:
                results.append({"transaction_date" : item["transactionDate"], "price" : item["pricePaid"], "address" : item["propertyAddress"], "new" : item["newBuild"], "street" : item["propertyAddress"]["street"]})
        else:
            msg = "Api fail!"
        return jsonify(msg = msg, result = results)
    except:
        err_msg = traceback.format_exc()
        mylog(msg = "/house/price:" + err_msg, file = "error.log", handler = 0b10)
        return jsonify(msg = "Internal error!", result = results)

        



