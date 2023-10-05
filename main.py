import json
from flask import Flask, jsonify, request
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin
from verifiers.verifyRoteiro import  verifyAllItemsIsDone
from pymongo.mongo_client import MongoClient
MONGO_URI = "mongodb+srv://matheusfcarvalho2001:3648@cluster0.rioem39.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)

db = client['pequi']

collection = db['roteiro']

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    routeInformations = collection.find_one()
    if routeInformations:
        routeInformations['_id'] = str(routeInformations['_id'])
    # return jsonify(routeInformations)
    return jsonify({'routeInformations':routeInformations})

# rota de confirmação de rota

# rota de relatar problema

@app.route('/confirm/<idRoteiro>/<int:idPedido>/<int:index>', methods=['PUT'])
@cross_origin()
def confirm(idRoteiro, idPedido, index):
    try:
        # import ipdb; ipdb.set_trace()
        roteiroId = ObjectId(idRoteiro)
        roteiro = collection.find_one({'_id':roteiroId})
        roteiro['pedidos'][idPedido]['pedidos'][index]['isDone'] = True
        
        items = roteiro['pedidos'][idPedido]['pedidos']
        if verifyAllItemsIsDone(items):
            roteiro['pedidos'][idPedido]['isDone'] = True

        response = collection.update_one({'_id':roteiroId},{'$set':roteiro})
        # Faça o que você precisa com os dados
        print(response)

        newRoteiro = roteiro
        
        newRoteiro['_id'] = str(newRoteiro['_id'])

        response_data = {'message': 'Dados recebidos com sucesso', 'newRoteiro':newRoteiro}
        return jsonify(response_data), 200
    except KeyError:
        # Se algum dos campos estiver faltando no corpo da requisição, retorne um erro
        return jsonify({'error': 'Campos ausentes no corpo da requisição'}), 400
    except Exception as e:
        # Lida com outros erros que podem ocorrer durante o processamento
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
