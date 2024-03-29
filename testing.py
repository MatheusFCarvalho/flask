import re
import json

def parse_text_to_mongodb_doc(text):
    newtext = text.replace("\u00e7", "C")
    newnewtext = newtext.replace("\u00c7", "C")
    lines = newnewtext.strip().split('\n')
    deliveries = []
    total_entregas = 0
    total_pecas = 0

    current_delivery = None
    current_items = []

    for line in lines:
        if line.startswith("CLIENTE"):
            if current_delivery is not None:
                current_delivery["itens"] = current_items
                deliveries.append(current_delivery)
            current_delivery = {}
            current_items = []
            continue

        if current_delivery is not None:
            parts = line.split("\t")
            if len(parts) >= 5:
                # import ipdb; ipdb.set_trace()
                cliente = parts[0]
                pedido = int(parts[1])
                pecas = int(parts[2])
                endereco = parts[4]
                obs = parts[5]
                if cliente == '':
                    lastItem = current_items[-1]
                    lastItem['pedidos'].append(pedido)
                    lastItem['pecas'] += pecas
                else:
                    item = {
                        "cliente": cliente,
                        "pedidos": [pedido],
                        "pedidosFeito":[],
                        "pecas": pecas,
                        "endereco": endereco,
                        "obs": obs,
                        "isError": False,
                        "isDone": False,
                        "messagesError":[]
                    }
                    current_items.append(item)
                total_entregas += 1
                total_pecas += pecas
                
    if current_delivery is not None:
        current_delivery["itens"] = current_items
        deliveries.append(current_delivery)

    title = lines[0]
    # title = title.split('\t')[0]
    mongodb_doc = {
        "title":title.replace('\t',''),
        "pedidos": current_items,
        "total_entregas": total_entregas,
        "total_pecas": total_pecas
    }

    return json.dumps(mongodb_doc, indent=2)

# Exemplo de uso:
text = """
ENTREGAS 17-10 --- ZONA LESTE 					
CLIENTE 	PEDIDO	PEÇAS	SEPARADOR	ENDEREÇO 	OBS:
IN VITRO 	23054	3		RUA MARIA APARECIDA DO CARMO SILVA - 25 	LIBERADO
	23049	1			
ESQUALY VALE 	23079	11		COLOCAR ENDEREÇO NO SISTEMA 	RECEBER
	22962	1			
BELO DESIGN 	23062	4		AV UBERABA - 269 JD ISMÊNIA	RECEBER
TIAGO SANTA MARIA 	23091	4		COLOCAR ENDEREÇO NO SISTEMA 	LIBERADO
MOVELARIA TOP VALE 	23164	1		COLOCAR ENDEREÇO NO SISTEMA 	RECEBER
2M MOVELARIA 	23188	2		AV PRES. TANCREDO NEVES -797	LIBERADO
CAVALCANTE 	23057	1		RUA BENEDITO FERNANDES DE ANDRADE - 65	LIBERADO
	23143	5			
	23130	4			
MARCENARIA JOSEENSE 	23148	2		RUA HELEODORA PEREIRA LEMES - 77 	RECEBER
"""

# mongodb_doc = parse_text_to_mongodb_doc(text)
# print(mongodb_doc)
# from pymongo.mongo_client import MongoClient
# from bson.objectid import ObjectId

# MONGO_URI = "mongodb+srv://matheusfcarvalho2001:3648@cluster0.rioem39.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(MONGO_URI)
# db = client['pequi']
# collection = db['usuarios']

# userId = ObjectId('651f06b25a14ba6cead36a05')
# user = collection.find_one({'_id':userId})
# user['isAdmin'] = True
# collection.update_one({'_id':userId},{'$set':user})

# collectionGuide = db['guideLiner']
# collectionGuide.insert_one({'guideOf':'route', 'routeId':routeId})


def testing(str):
    arr = []
    for s in str:
        arr.append(s)
    for n,pos in enumerate(arr):
        arr[n] = pos
    print(arr)
# testing('batata')
def testing2(str):
    for s in str:
        str += str
    print(str)
# testing2('batata')

def testing3(str):
    for s in str:
        str = str.replace(s,str)
        print(len(str))
# testing3('12434')

def testArr(arr):
    for ind, elem in enumerate(arr):
        arr[ind] = str(arr)  # Convert the individual element to a string

    save = ''.join(arr)
    print(save)
    print(len(save))

testArr([2, 1, 3])


# import plotly.express as px

# data = {
#     "1": {
#         "data": "2023/01",
#         "tatiane brockyeld": {"totalVendido": 110236.62, "qtdVendas": 200},
#         "michelle boschetti": {"totalVendido": 148429.63, "qtdVendas": 144},
#         "juliana madeira": {"totalVendido": 280.26, "qtdVendas": 1},
#         "luciana rocha": {"totalVendido": 48293.60, "qtdVendas": 43},
#         "bianca boschetti": {"totalVendido": 24794.81, "qtdVendas": 41},
#     }
# }

# # Extrair os nomes dos vendedores e os totais vendidos
# vendors = []
# totals = []
# for vendor, info in data["1"].items():
#     if vendor != "data":
#         vendors.append(vendor)
#         totals.append(info["totalVendido"])

# fig = px.bar(data_frame=data, x=vendors, y=totals, title="Total Vendido por Vendedor em Janeiro de 2023")
# fig.update_xaxes(title_text="Vendedor")
# fig.update_yaxes(title_text="Total Vendido")
# fig.show()