import json
from flask import Flask, jsonify, request
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin
from verifiers.verifyRoteiro import  verifyAllItemsIsDone
from pymongo.mongo_client import MongoClient
from routes import loginsRoutes, crudRoutes, excelRoutes
from verifiers.verifyToken import token_required
import requests
from functions.getLoginWvetro import getTokenWvetro
from dotenv import load_dotenv
import os

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
SECRET_KEY = os.getenv("SECRET_KEY")

# Conectar ao MongoDB
client = MongoClient(MONGO_URI)

db = client['pequi']

collection = db['roteiro']
collecctionExcel = db['route']


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY  # Defina uma chave secreta segura
# CORS(app)
CORS(app)

# DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED
@app.route('/')
def index():
    routeInformations = collection.find_one({'roteiroHoje':True})
    roteiroId = routeInformations['idRoteiro']
    roteiro = collection.find_one({'_id':roteiroId})
    if roteiro:
        roteiro['_id'] = str(roteiro['_id'])
    # return jsonify(routeInformations)
    return jsonify({'routeInformations':roteiro})
# DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED DEPRECATED


@app.route('/setRoteiro/<idRoteiro>')
def setRoteiro(idRoteiro):
    try:
        routeInformations = collection.find_one({'roteiroHoje':True})
        print(routeInformations)
        routeInformations['idRoteiro'] = ObjectId(idRoteiro)
        print(routeInformations)
        collection.update_one({'_id':routeInformations['_id']}, {'$set':routeInformations})
        return jsonify({'deu': 'certo'})
    except:
        return jsonify({'error': 'id não encontrado'}), 401

@app.route('/<int:roteiroId>')
@token_required
def specifRoute(roteiroId):
    routeInformations = collection.find_one({'roteiroId':roteiroId})
    if routeInformations:
        routeInformations['_id'] = str(routeInformations['_id'])
    # return jsonify(routeInformations)
    return jsonify({'routeInformations':routeInformations})

# rota de confirmação de rota

@app.route('/confirm/<idRoteiro>/<int:idPedido>/<int:index>', methods=['PUT'])
@cross_origin()
@token_required
def confirm(idRoteiro, idPedido, index):
    try:
        # import ipdb; ipdb.set_trace()
        roteiroId = ObjectId(idRoteiro)
        roteiro = collection.find_one({'_id':roteiroId})
        roteiro['pedidos'][idPedido]['pedidos'][index]['isDone'] = True
        
        items = roteiro['pedidos'][idPedido]['pedidos']
        if verifyAllItemsIsDone(items):
            roteiro['pedidos'][idPedido]['isDone'] = True
        
        collection.update_one({'_id':roteiroId},{'$set':roteiro})

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


@app.route('/problem/<idRoteiro>/<idPedido>', methods=['PUT'])
@cross_origin()
@token_required
def problem(idRoteiro, idPedido):
    try:
        data = request.get_json()  # Obtenha os dados JSON do corpo da solicitação

        messageError = data.get('messageError')  # Acesse 'messageError' dos dados JSON
        
        roteiroId = ObjectId(idRoteiro)
        roteiro = collection.find_one({'_id':roteiroId})
        roteiro['pedidos'][int(idPedido)]['messagesError'].append(messageError)
        roteiro['pedidos'][int(idPedido)]['isError'] = True
        
        collection.update_one({'_id':roteiroId},{'$set':roteiro})

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


app.register_blueprint(loginsRoutes.bp, url_prefix = '/login')
app.register_blueprint(crudRoutes.bp, url_prefix = '/cruds')
app.register_blueprint(excelRoutes.bp, url_prefix = '/excels')

if __name__ == '__main__':
    app.run(debug=True)
