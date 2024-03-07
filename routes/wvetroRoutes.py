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
