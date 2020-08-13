from flask import jsonify
from helpers.myutils import getSKP
from flask import request


def testRoute(id):
    return jsonify({"test": "ok", "id": id})


def getHome():
    return jsonify({"test": "ok", "skp": getSKP(request.headers)})
