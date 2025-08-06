from flask import Flask, jsonify, request, abort, render_template

app = Flask("__main__")

# in-memory database
items=[
    {'id':1, "name":"Laptop", "price":40000},
    {'id':2, "name":"Iphone", "price":50000}
    ]

@app.route("/")
def home():
    return {"message":"Welcome to Flask Rest API."}


# get all items
@app.route("/items", methods=['GET'])
def getitems():
    return jsonify(items)
    

# get item by ID
@app.route("/items/<int:itemid>", methods=["GET"])
def get_item(itemid):
    item = next((i for i in items if i['id']==itemid), None)
    if item:
        return jsonify(item)
    abort(404, description="Item Not Found")
    
@app.route("/items", methods=["POST"])
def createitems():
    data=request.get_json()
    if not data or "price" not in data or "name" not in data:
        abort(404, description="Invalid input")
    newid = items[-1]['id'] + 1 if items else 1
    item = {'id': newid,
            'name': request.json['name'],
            'price': float(request.json['price'])
    }
    items.append(item)
    return jsonify(item), 201

@app.route("/items:/<int:itemid>",methods=["PUT"])
def update_items(itemid):
    item = next((i for i in items if i['id']==itemid), None)
    if item is None:
        abort(404)
    if not request.json:
        abort(404)
    item['name']=request.json.get('name', item['name'])
    item['price']=float(request.json.get('price', item['price']))
    return jsonify(item)


#delte items
@app.route("/items/<int:itemid>", methods=["DELETE"])
def delete_items(itemid):
    global items
    items = [i for i in items if i['id'] != itemid]
    return jsonify({"message": "Item deleted"})

if __name__=="__main__":
    app.run(debug=True)
