from functools import wraps
from flask import session, jsonify
from dotenv import load_dotenv
# import jwt

load_dotenv()

def mySession_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session['isLogin']:
            return f(*args, **kwargs)
            return True
        else:
            return jsonify({'message': 'precisa estar logado!'})

        if not token:
            return jsonify({'message': 'Token está faltando!'}), 401

        try:
            token = token.split(' ')[1]
            # data = jwt.decode(token, key='hellokitty', algorithms='HS256')
        except:
            return jsonify({'message': 'Token é inválido!'}), 401

        return f(*args, **kwargs)

    return decorated
