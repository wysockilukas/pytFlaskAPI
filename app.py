from flask import Flask, jsonify, request
import sys
import os
import datetime
import atexit

# import configparser

from helpers.myutils import config, getSKP, logInfo, xlsx_to_response
from RouteControllers.mainRoute import testRoute, getHome
from RouteControllers.oracleRoute import getOracleSql

app = Flask(__name__)


# sys.path.append("/app/odbclient/product/12.1.0/client_1/")
# sys.path.append("/app/odbclient/product/12.1.0/client_1/lib/")
# os.environ["ORACLE_HOME"] = "/app/odbclient/product/12.1.0/client_1/"


# config = configparser.ConfigParser()
# config.read("config.ini")
base = config["DEFAULT"]["BASE"]
print("****\nStart aplikacji\n****\n")


app.add_url_rule(base, "getHome", getHome)
app.add_url_rule("/test/<string:id>", "testRoute", testRoute)
app.add_url_rule(base + "/oracle/<string:id>", "getOracleSql", getOracleSql)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": 404}), 404


# @app.route(base + "/store", methods=["POST"])
# def create_store():
#     request_data = request.get_json()
#     new_store = {"name": request_data["name"], "items": []}
#     stores.append(new_store)
#     return jsonify({"stores": stores})


app.run(host="0.0.0.0", port=9661)


# https://cx-oracle.readthedocs.io/en/latest/user_guide/connection_handling.html#establishing-database-connections

