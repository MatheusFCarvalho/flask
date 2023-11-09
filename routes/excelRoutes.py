from pymongo.mongo_client import MongoClient
from flask import request, jsonify, request, Blueprint
from verifiers.verifyToken import token_required
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin
from functions.documentsMaker import parse_text_to_mongodb_doc
from verifiers.verifyRoteiro import  verifyAllItemsIsDoneExcel, verifyIfCanAddRequest
from dotenv import load_dotenv
import os

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Conectar ao MongoDB
client = MongoClient(MONGO_URI)
db = client['pequi']
collection = db['route']
collectionGuide = db['guideLiner']

bp = Blueprint('excels', __name__)
CORS(bp, resources={r"/": {"origins": "http://localhost:3000"}})


@bp.route('/' ,methods=['GET'])
@cross_origin(origin='*')
def getRoute():
    routeInformations = collectionGuide.find_one({'guideOf':'route'})
    roteiroId = routeInformations['routeId']
    roteiro = collection.find_one({'_id':roteiroId})
    if roteiro:
        roteiro['_id'] = str(roteiro['_id'])
        roteiro['id'] = roteiro.pop('_id')
    # return jsonify(routeInformations)
    return jsonify({'routeInformations':roteiro})

@bp.route('/create' ,methods=['POST'])
def createByExcelText():
    text = request.json['exceldata']
    document = parse_text_to_mongodb_doc(text)
    result = collection.insert_one(document)
    routeId = str(result.inserted_id)
    return routeId





@bp.route('/confirm/<idRoteiro>/<int:idPedido>/<int:number>', methods=['PUT'])
@cross_origin()
@token_required
def confirm(idRoteiro, idPedido, number):
    try:
        # import ipdb; ipdb.set_trace()
        roteiroId = ObjectId(idRoteiro)
        roteiro = collection.find_one({'_id':roteiroId})

        pedido = roteiro['pedidos'][idPedido]
        if verifyIfCanAddRequest(pedido, number):
            roteiro['pedidos'][idPedido]['pedidosFeito'].append(number)
        # roteiro['pedidos'][idPedido]['pedidos'][index]['isDone'] = True
        
        pedido = roteiro['pedidos'][idPedido]
        if verifyAllItemsIsDoneExcel(pedido):
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


@bp.route('/problem/<idRoteiro>/<idPedido>', methods=['PUT'])
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



@bp.route('/allRoteiro', methods=['GET'])
def getAllRoteiro():
    pipeline = [
        {
            '$project': {
                '_id': 0,  # Exclui o campo '_id' original
                'id': '$_id',  # Renomeia '_id' para 'id'
                'title': 1,
            }
        }
    ]
    cursor = collection.aggregate(pipeline)
    
    # Crie uma lista com os resultados
    resultado = []
    for documento in cursor:
        documento['id'] = str(documento['id'])
        resultado.append(documento)
    
    # Retorne a lista como uma resposta JSON
    return jsonify(resultado)



@bp.route('/oneRoteiro/<idRoteiro>', methods=['GET'])
def retornarRoteiro(idRoteiro):
    try:
        roteiroId = ObjectId(idRoteiro)
        roteiro = collection.find_one({'_id':roteiroId})
        roteiro['_id'] = str(roteiro['_id'])
        roteiro['id'] = roteiro.pop('_id')
        return roteiro
    except Exception as e:
        return jsonify({'error': str(e)})


@bp.route('/setRoteiro/<idRoteiro>', methods=['PUT'])
def setRoteiro(idRoteiro):
    try:
        routeInformations = collectionGuide.find_one({'guideOf':'route'})
        routeInformations['routeId'] = ObjectId(idRoteiro)
        collectionGuide.update_one({'_id':routeInformations['_id']}, {'$set':routeInformations})
        return jsonify({'deu': 'certo'})
    except:
        return jsonify({'error': 'id não encontrado'}), 401
