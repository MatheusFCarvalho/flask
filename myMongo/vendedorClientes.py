from pymongo.mongo_client import MongoClient
MONGO_URI = "mongodb+srv://matheusfcarvalho2001:3648@cluster0.rioem39.mongodb.net/?retryWrites=true&w=majority"
# "mongodb+srv://matheusfcarvalho2001:<password>@cluster0.rioem39.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)

db = client['pequi']

collection = db['vendedores']

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