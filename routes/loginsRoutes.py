from datetime import date
from flask import render_template, redirect
from flask import jsonify, request, Blueprint
from verifiers.verifyToken import mySession_required
from dotenv import load_dotenv
# from bson.objectid import ObjectId
# from . import usuariosCollection
# import jwt
# import datetime
# import bcrypt
# from flask_cors import CORS
# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

regi_bp = Blueprint('register', __name__)
auth_bp = Blueprint('logs', __name__)
# CORS(bp)

# Rota para cadastro de usuário
@regi_bp.route('/register', methods=['POST'])
def registrar_usuario():

    return jsonify({'message': 'Usuário nao registrado com sucesso!'}), 201

@auth_bp.route('/', methods=['GET'])
@auth_bp.route('/login/', methods=['GET'])
def login():
    return render_template('auth/login.html')

@regi_bp.route('/login/post/', methods='[POST]')
def loginPost():
    hoje = date.today()
    hojeStr = hoje.strftime('%d%m%Y')
    dictForm = request.form.to_dict()
    dictForm['idDia'] = hojeStr
    
    return render_template('login/post.html', dictInfo=dictForm)


@auth_bp.route('/getMyUser/<userId>')
@mySession_required
def getInfoUser(userId):
    infoUser = getInfoUser(userId)
    return jsonify({'userInfo': infoUser})


@auth_bp.route('/protegida')
@mySession_required
def protegida():
    return jsonify({'message': 'Rota protegida!'})

if __name__ == '__main__':
    auth_bp.run(debug=True)
    regi_bp.run(debug=True)