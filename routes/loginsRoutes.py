from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from flask_pymongo import PyMongo
import jwt
import datetime
import bcrypt
from flask import request, jsonify, request, Blueprint
from verifiers.verifyToken import token_required
from bson.objectid import ObjectId

# Função para verificar se o usuário está autenticado

MONGO_URI = "mongodb+srv://matheusfcarvalho2001:3648@cluster0.rioem39.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['pequi']
collection = db['usuarios']

bp = Blueprint('logs', __name__)

# Rota para cadastro de usuário
@bp.route('/registro', methods=['POST'])
def registrar_usuario():
    data = request.get_json()

    # Verifique se o usuário já existe
    if collection.find_one({'username': data['username']}):
        return jsonify({'message': 'Nome de usuário já está em uso!'}), 400

    # Faça o hash da senha
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    # Crie um novo usuário com a senha hasheada
    data['password'] = hashed_password.decode('utf-8')
    collection.insert_one(data)

    return jsonify({'message': 'Usuário registrado com sucesso!'}), 201

# Rota para fazer login e obter um token JWT (mantida da implementação anterior)
@bp.route('/', methods=['POST'])
def login():
    data = request.get_json()
    
    usuario = collection.find_one({'username': data['username']})

    if usuario and bcrypt.checkpw(data['password'].encode('utf-8'), usuario['password'].encode('utf-8')):
        usuario['_id'] = str(usuario['_id'])
        token = jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5),
            'iat':datetime.datetime.utcnow(),
            'sub': usuario['_id'],
             }, key='hellokitty', algorithm='HS256')


        return jsonify({'token': token}), 201

    return jsonify({'message': 'Credenciais inválidas'}), 401

# Rota protegida que requer autenticação (mantida da implementação anterior)

@bp.route('/getMyUser')
@token_required
def getInfoUser():
    data = request.get_json()  # Obtenha os dados JSON do corpo da solicitação

    userId = data.get('userId')  # Acesse 'messageError' dos dados JSON
    user = collection.find_one({'_id':ObjectId(userId)})

    return jsonify({'userInfo': user})


@bp.route('/protegida')
@token_required
def protegida():
    return jsonify({'message': 'Rota protegida!'})

if __name__ == '__main__':
    bp.run(debug=True)
