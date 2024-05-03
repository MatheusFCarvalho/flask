from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

MONGO_URI = os.getenv('MONG_URI')
DATABASE = os.getenv('DATABASE')

client = MongoClient(MONGO_URI)

db = client[DATABASE]

collection = db['vendedores']

class RepositorierOfAll:
    def __init__(self, database):
        self.database = database
        self.collectionsDict = dict()
        self.collectionsArr = list()

    def adicionarCollection(self, keyOfCollection):
        collection = self.database[keyOfCollection]
        self.collectionsDict[keyOfCollection] = collection
        self.collectionsArr.append(collection)
        return collection
    def adicionarDocumento(self, documento, guiaCollection = 0):
        if guiaCollection.isinstance(str):
            self.collectionsDict[guiaCollection].insert_one(documento)
        elif guiaCollection.isinstance(int):
            self.collectionsArr[guiaCollection].insert_one(documento)

def adicionar_clientes(vendedor, novos_clientes):
    # Atualiza o documento específico usando find_one_and_update
    collection.find_one_and_update(
        {'tipo': 'clientesAtuais', 'vendedor': vendedor},
        {'$addToSet': {'clientes': {'$each': novos_clientes}}},
        upsert=True  # Cria o documento se não existir
    )


# mesesAvaliados = ['2024/01', '2023/12', '2023/12']
# # mesesAvaliados = ['2024/01']
# notSellers = ['_id', 'data', 'clientesDb', 'lastUpdate', 'pedidosId', 'updatedBy']

# for mes in mesesAvaliados:
#     docOfMes = collection.find_one({'data':mes})
#     sellers = [seller for seller in docOfMes.keys() if seller not in notSellers]
#     for seller in sellers:
#         clientes = docOfMes[seller]['clientes']
#         adicionar_clientes(seller,clientes)
#     # import ipdb; ipdb.set_trace()


# print('finalized')