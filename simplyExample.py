from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [{"name": "My Store", "items": [{"name": "my item", "price": 15.99}]}]

print("Tu jestem")


@app.route(
    "/"
)  # tp jest decorator wiec ta funckja pod spodem jest przekazywan do funcjcji @app.route
def home():
    # return "hej"
    return render_template("index.html")


# post /store data: {name :}
@app.route("/store", methods=["POST"])
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return jsonify({"stores": stores})


# pass


# get /store/<name> data: {name :}
@app.route("/store/<string:name>")
def get_store(name):
    print("W gunckji")
    print(name)
    for store in stores:
        if store["name"] == name:
            return jsonify(store)
    return jsonify({"message": "store not found 2", "szukane": name})


# pass


# get /store
@app.route("/store")
def get_stores():
    return jsonify({"stores": stores})


# return jsonify(stores)


# post /store/<name> data: {name :}
@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return jsonify(new_item)
    return jsonify({"message": "store not found"})


# pass


# get /store/<name>/item data: {name :}
@app.route("/store/<string:name>/item")
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({"items": store["items"]})
    return jsonify({"message": "store not found"})


# pass


app.run(port=5000)
