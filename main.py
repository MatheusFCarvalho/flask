from flask import Flask, jsonify
from myMongo.connection import collection
from bson import ObjectId

from flask_cors import CORS

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
    dailyInformations = collection.find_one()
    if dailyInformations:
        dailyInformations['_id'] = str(dailyInformations['_id'])
    # return jsonify(dailyInformations)
    return jsonify({'dailyInformations':dailyInformations})

# @app.route('/onlyMongo')
# def onlyMongo():
#     return jsonify(rotaDayData)


if __name__ == '__main__':
    app.run(debug=True)
