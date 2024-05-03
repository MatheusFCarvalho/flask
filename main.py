from flask import Flask, jsonify
from routes import loginsRoutes, sellersRoutes

app = Flask(__name__)

# app.register_blueprint(loginsRoutes.auth_bp, url_prefix = '/login')
# app.register_blueprint(loginsRoutes.regi_bp, url_prefix = '/register')
app.register_blueprint(sellersRoutes.sell_bp, url_prefix = '/sellers')


@app.route("/")
def hello():
    return jsonify('Seguinte, mudanças aconteceram neste site! agora é necessario atrelar sua conta do pcSite aqui! duvidas conversar com pcp!')
    return "Hello World!"

if __name__ == "__main__":
    app.run()
    
    # import json
# from flask import Flask, jsonify
# from dotenv import load_dotenv
# import os
# from flask import Flask, render_template

# from flask_cors import CORS
# from flask_socketio import SocketIO, emit
# Carregue as variáveis de ambiente do arquivo .env
# load_dotenv()

# SECRET_KEY = os.getenv("SECRET_KEY")

# app = Flask(__name__)
# socketio = SocketIO(app)

# app.config['SECRET_KEY'] = SECRET_KEY  # Defina uma chave secreta segura
# CORS(app)
# app.route('/', methods=['GET'])
# app.route('/duck/', methods=['GET'])
# def index():

# app.register_blueprint(sellersRoutes.bp, url_prefix = '/sellers')

# if __name__ == '__main__':
    # socketio.run(app, debug=True)
    # app.run(debug=True)
