from functools import wraps
from flask import request, jsonify
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token está faltando!'}), 401

        try:
            token = token.split(' ')[1]
            data = jwt.decode(token, key='hellokitty', algorithms='HS256')
        except:
            return jsonify({'message': 'Token é inválido!'}), 401

        return f(*args, **kwargs)

    return decorated
