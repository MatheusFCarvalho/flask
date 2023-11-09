import json
from flask import Flask
from flask_cors import CORS
from routes import loginsRoutes, excelRoutes, webChatRoutes
from dotenv import load_dotenv
import os

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY  # Defina uma chave secreta segura
CORS(app)

app.register_blueprint(loginsRoutes.bp, url_prefix = '/login')
app.register_blueprint(excelRoutes.bp, url_prefix = '/excels')
app.register_blueprint(webChatRoutes.bp, url_prefix = '/webChat')

if __name__ == '__main__':
    app.run(debug=True)
