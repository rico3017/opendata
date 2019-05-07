from flask import Blueprint, jsonify, request,abort
from myconfig import page_size, apis, app_id, app_key
from myutil.mylog import mylog
import requests, datetime, json, traceback
from urllib import parse

mod = Blueprint("london", __name__, url_prefix="/london")

'''
@mod.route("/streets/", methods = ["POST", "GET"])
def streets():
    try:
        results = []
        if "postcode" not in request.values:
            abort(416)
        params = {}
        params["app_id"] = app_id
        params["app_key"] = app_key
        url = apis["ttl"] + "/Place/Address/Streets/" + request.values["postcode"].upper()
        mylog(msg = "/london/streets:" + json.dumps(params) + '|' + request.values["postcode"], file = "send.log", handler = 0b10)
        res = requests.get(url, params = params)
        mylog(msg = "/london/streets:" + str(res.content), file = "receive.log", handler = 0b10)
        if res.status_code == 200:
            msg = "success"
        else:
            msg = "Api fail!"
        results = res.json()
        return jsonify(msg = msg, result = results)
    except Exception as e:
        err_msg = traceback.format_exc()
        mylog(msg = "/london/streets:" + err_msg, file = "error.log", handler = 0b10)
        return jsonify(msg = "Error!", result = results)
'''


@mod.route("/nearbyTrans/", methods = ["POST", "GET"])
def nearbyTrans():
    try:
        results = []
        if "street" not in request.values:
            abort(416)
        params = {}
        params["app_id"] = app_id
        params["app_key"] = app_key
        url = apis["ttl"] + "/StopPoint/Search/" + request.values["street"] #%20
        mylog(msg ="request url:" + url + "|" + "/london/streets:" + json.dumps(params) + '|' + request.values["street"], file = "send.log", handler = 0b10)
        res = requests.get(url, params = params)
        mylog(msg = "request url:" + url + "|" + "/london/streets:" + str(res.content), file = "receive.log", handler = 0b10)
        if res.status_code == 200:
            dic = res.json()
            ids = dic["matches"]
            stop = len(ids)
            if stop > 20:
                stop = 20
            id_str = ""
            for i in range(0, stop):
                id_str += ids[i]["id"]
                id_str += "," #%2C%
            if stop > 0:
                url2 = apis["ttl"] + "/StopPoint/" + id_str
                mylog(msg ="request url:" + url2 + "|" + "/london/streets:" + json.dumps(params) + '|' + request.values["street"], file = "send.log", handler = 0b10)
                res2 = requests.get(url2, params = params)
                mylog(msg = "request url:" + url2 + "|" + "/london/streets:" + str(res2.content), file = "receive.log", handler = 0b10)
                if res2.status_code == 200:
                    msg = "success"
                    items = res2.json()
                    if stop > 1:
                        for item in items:
                            temp = []
                            groups = item["lineModeGroups"]
                            for var in groups:
                                temp.append({"lines" : var["lineIdentifier"], "mode" : var["modeName"]})
                            results.append({"groups" : temp, "id" : item["naptanId"], "name" : item["commonName"], "lat" : item["lat"], "lon" : item["lon"]})
                    else:
                        temp = []
                        groups = groups = items["lineModeGroups"]
                        for var in groups:
                            temp.append({"lines" : var["lineIdentifier"], "mode" : var["modeName"]})
                        results.append({"groups" : temp, "id" : items["naptanId"], "name" : items["commonName"], "lat" : items["lat"], "lon" : items["lon"]})
                else:
                    msg = "Api fail!"
            else:
                msg = "No bus data!"
        else:
            msg = "Api fail!"
        return jsonify(msg = msg, result = results)
    except Exception as e:
        err_msg = traceback.format_exc()
        mylog(msg = "/london/streets:" + err_msg, file = "error.log", handler = 0b10)
        return jsonify(msg = "Error!", result = results)

@mod.route("/getloc/", methods = ["POST", "GET"])
def getloc():
    try :
        result = {}
        if "postcode" not in request.values:
            abort(416)
        url = apis["postcode"] + "/postcodes/" +  request.values["postcode"].upper()
        res = requests.get(url)
        mylog(msg = "request url:" + url + "|" + "/london/streets:" + str(res.content), file = "receive.log", handler = 0b10)
        if res.status_code == 200:
            dic = res.json()
            result["lon"] = dic["result"]["longitude"]
            result["lat"] = dic["result"]["latitude"]
        elif res.status_code == 404:
            msg = "Invalid postcode!"
        else:
            msg = "Api fail!"
        return jsonify(msg = msg, result = result)

    except:
        err_msg = traceback.format_exc()
        mylog(msg = "/london/streets:" + err_msg, file = "error.log", handler = 0b10)
        return jsonify(msg = "Error!", result = result) 