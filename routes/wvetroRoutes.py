from pymongo.mongo_client import MongoClient
from flask import request, jsonify, request, Blueprint
from flask_cors import CORS, cross_origin
from functions.documentsMaker import parse_text_to_mongodb_doc
from verifiers.verifyRoteiro import  verifyAllItemsIsDoneExcel, verifyIfCanAddRequest, verifyIfExcelAreRight
from dotenv import load_dotenv
import os

# Carregue as variáveis de ambiente do arquivo .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Conectar ao MongoDB
client = MongoClient(MONGO_URI)
db = client['pequi']
collection = db['routeCheker']
collectionGuide = db['guideLiner']

# conversa e concentração, não consigo escutar la onde gostaria, não consigo bisbilhotar muito bem quem diria, e agora fica confuso perdido obtuso, chegou um cliente, inclusive, nossa mas que bagunça, taltaltal taltaltal
bp = Blueprint('wvetro_routes', __name__)

# Defina a rota para receber os dados
@bp.route('/create', methods=['POST'])
def receber_dados():
    data = request.json  # Obter os dados enviados pela extensão
    # Aqui você pode processar os dada necessário
    # Por exemplo, salvar em um banco de dados ou realizar outras operações
    import ipdb; ipdb.set_trace()
    print(data)
    # Retornar uma resposta (opcional)
    return jsonify({'message': 'Dados recebidos com sucesso'}), 200

# qual sera a primeira coisa que ele vai falar? bom eu n sei, ele murmurou algo ou sussurrou, bom n sei a, n etendi mas foi c tati,
