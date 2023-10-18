from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from flask_pymongo import PyMongo
import jwt
import datetime
import bcrypt
from flask import request, jsonify, request, Blueprint
from verifiers.verifyToken import token_required
from verifiers.verifyRoteiro import verifyIfClientAlreadyExist
from bson.objectid import ObjectId
import requests
from flask_cors import CORS, cross_origin
from functions.getLoginWvetro import getTokenWvetro
from functions.documentsMaker import parse_text_to_mongodb_doc
from dotenv import load_dotenv
import os

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client['pequi']
collection = db['roteiro']

bp = Blueprint('cruds', __name__)
CORS(bp)


@bp.route('/allRoteiro', methods=['GET'])
def getAllRoteiro():
    pipeline = [
        {
            '$project': {
                '_id': 0,  # Exclui o campo '_id' original
                'id': '$_id',  # Renomeia '_id' para 'id'
                'data': 1,
                # 'title': 1,
                'roteiroId': 1
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
        print(roteiro)
        return roteiro
    except Exception as e:
        return jsonify({'error': str(e)})



@bp.route('/create', methods=['POST'])
def criarRoteiro():
    data = request.get_json()
    data['pedidos'] = []
    response = collection.insert_one(data)
    id = response.inserted_id

    roteiro = collection.find_one({'_id':id})
    roteiro['id'] = roteiro.pop('_id')
    roteiro['id'] = str(roteiro['id'])
    print(roteiro)
    return jsonify(roteiro), 201

@bp.route('/insertOrder/<idRoteiro>', methods=['PUT'])
def adicionarPedido(idRoteiro):
    data = request.get_json()
    pedidoReturn = {
        'cliente':'',
        'isDone': False,
        'isError': False,
        'messagesError': [],
        'pedidos': []
    }
    wvetroId = data['numero']

    token = getTokenWvetro()
    headers = {
        'Token':token,
    }
    url = 'https://sistema.wvetro.com.br/wvetro/rest/api/Pedidos/GetPedidoByKey?Orcamentoid=' + str(wvetroId)
    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()

        pedido = response_data["ListPedidos"][0]

        enderecoVetro = pedido["Endereco"]
        cliente = pedido["ClienteNome"]

        endereco = {}

        addressFields = ['Cidade', 'Bairro', 'Rua', 'Nro']
        for field in addressFields:
            if enderecoVetro[field] != "" and  enderecoVetro[field] != "S/N":
                endereco[field] = enderecoVetro[field]

        data['endereco'] = endereco

        pedidoReturn['cliente'] = cliente
        pedidoReturn['pedidos'] = [data]
    except Exception as e:
        return jsonify({'error': str(e)})



    print(data)
    roteiroId = ObjectId(idRoteiro)
    roteiro = collection.find_one({'_id':roteiroId})

    print(roteiro)

    roteiro = verifyIfClientAlreadyExist(roteiro, pedidoReturn)

    collection.update_one({'_id':roteiroId},{'$set':roteiro})

    roteiro['id'] = roteiro.pop('_id')
    roteiro['id'] = str(roteiro['id'])

    return jsonify(roteiro)

@bp.route('/deleteOrder/<idRoteiro>', methods=['PUT'])
def deleteOrder(idRoteiro):
    roteiroId = ObjectId(idRoteiro)
    clienteNome = request.get_json()
    roteiro = collection.find_one({'_id':roteiroId}) 
    newPedidos = []
    print('__'*80)
    print(roteiro)
    print('__'*80)
    for pedido in roteiro['pedidos']:
        if pedido['cliente'] != clienteNome:
            newPedidos.append(pedido)
    roteiro['pedidos'] = newPedidos

    collection.update_one({'_id':roteiroId},{'$set':roteiro})

    roteiro['id'] = roteiro.pop('_id')
    roteiro['id'] = str(roteiro['id'])
    
    return jsonify(roteiro)
