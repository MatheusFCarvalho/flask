from flask import Flask, jsonify
from bson import ObjectId
from flask_cors import CORS

from pymongo.mongo_client import MongoClient
MONGO_URI = "mongodb+srv://matheusfcarvalho2001:3648@cluster0.rioem39.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)

db = client['pequi']

collection = db['roteiro']

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    dailyInformations = collection.find_one()
    if dailyInformations:
        dailyInformations['_id'] = str(dailyInformations['_id'])
    # return jsonify(dailyInformations)
    return jsonify({'dailyInformations':dailyInformations})

@app.route('/confirm/')
def confirm():
    return jsonify({'dailyInformations':'chochooooo'})

# @app.route('/onlyMongo')
# def onlyMongo():
#     return jsonify(rotaDayData)


if __name__ == '__main__':
    app.run(debug=True)
