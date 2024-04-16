from flask import request, jsonify
import jwt
import datetime
import bcrypt
from flask import request, jsonify, request, Blueprint
from verifiers.verifyToken import token_required
from bson.objectid import ObjectId
from flask_cors import CORS
from dotenv import load_dotenv
from . import usuariosCollection
# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

bp = Blueprint('logs', __name__)
CORS(bp)

# Rota para cadastro de usuário
@bp.route('/registro', methods=['POST'])
def registrar_usuario():
    data = request.get_json()

    # Verifique se o usuário já existe
    if usuariosCollection.find_one({'username': data['username']}):
        return jsonify({'message': 'Nome de usuário já está em uso!'}), 400


    # Faça o hash da senha
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    # Crie um novo usuário com a senha hasheada
    data['password'] = hashed_password.decode('utf-8')
    usuariosCollection.insert_one(data)

    return jsonify({'message': 'Usuário registrado com sucesso!'}), 201

# Rota para fazer login e obter um token JWT (mantida da implementação anterior) 
@bp.route('/', methods=['POST'])
def login():
    data = request.get_json()

    usuario = usuariosCollection.find_one({'username': data['username']})
    if usuario and bcrypt.checkpw(data['password'].encode('utf-8'), usuario['password'].encode('utf-8')):
        usuario['_id'] = str(usuario['_id'])
        token = jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5),
            'iat':datetime.datetime.utcnow(),
            'sub': usuario['_id'],
             }, key='hellokitty', algorithm='HS256')

        userId = str(usuario['_id'])

        return jsonify({'token': token, 'userId':userId}), 201

    return jsonify({'message': 'Credenciais inválidas'}), 401
# Rota protegida que requer autenticação (mantida da implementação anterior)


@bp.route('/getMyUser/<userId>')
@token_required
def getInfoUser(userId):
    user = usuariosCollection.find_one({'_id':ObjectId(userId)})
    user['id'] = user.pop('_id')
    user['id'] = str(user['id'])
    user.pop('password')
    return jsonify({'userInfo': user})


@bp.route('/protegida')
@token_required
def protegida():
    return jsonify({'message': 'Rota protegida!'})

if __name__ == '__main__':
    bp.run(debug=True)
