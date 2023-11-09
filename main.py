import json
from flask import Flask
from flask_cors import CORS
from routes import loginsRoutes, excelRoutes, sellersRoutes
from dotenv import load_dotenv
import os
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, jsonify
# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
socketio = SocketIO(app)

app.config['SECRET_KEY'] = SECRET_KEY  # Defina uma chave secreta segura
CORS(app)

app.register_blueprint(loginsRoutes.bp, url_prefix = '/login')
app.register_blueprint(excelRoutes.bp, url_prefix = '/excels')
app.register_blueprint(sellersRoutes.bp, url_prefix = '/sellers')

if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run(debug=True)
