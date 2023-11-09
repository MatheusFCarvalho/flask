from pymongo.mongo_client import MongoClient
import requests
import datetime
from pymongo import MongoClient

def get_current_month_data(base_url, headers, db, reset = False):
    today = datetime.date.today()
    year = today.year
    month = today.month
    formatted_month = f'{month:02d}'

    existing_data = db.find_one({"data": f'{year}/{formatted_month}'})

    # if reset or not existing_data:
    # documentOfTime = {'data': f'{year}/{formatted_month}',
    #                         'pedidosId': [],
    #                         'clientesDb':{}}
    # else:
    #     documentOfTime = existing_data
 
    # Construa a URL para a requisição com base no mês atual
    url = f'{base_url}Pedidos/ListPedidos?Dtvendainicial={year}-{formatted_month}-01&Dtvendafinal={year}-{formatted_month}-31'

    # Faça a requisição
    response = requests.get(url, headers=headers)

    from examples import exampleOfClientesDb    
    if response.status_code == 200:
        # Trate os dados da resposta
        data = response.json()
        allPedidos = data['ListPedidos']
        documentOfTime = {'data': f'{year}/{formatted_month}', 'pedidosId':[], 'clientesDb':exampleOfClientesDb}
        
        for pedido in allPedidos:
            nroPedido = pedido['Nro']
            clientName = pedido['ClienteNome']
            if not nroPedido in documentOfTime['pedidosId']:
                vendedorName = pedido['VendedorNome'].lower()
                
                documentOfTime['pedidosId'].append(nroPedido)
                documentOfTime = addBasicData(documentOfTime, pedido, vendedorName, clientName)

                documentOfTime = addPortaDados(documentOfTime, pedido, vendedorName)

        # Gere o ranking

        documentOfTime = addPercentageCliente(documentOfTime)
        documentOfTime = generate_ranking(documentOfTime)

        # Atualize o documento no MongoDB
        db.update_one({"data": documentOfTime["data"]}, {"$set": documentOfTime}, upsert=True)

        return "Dados coletados, tratados e atualizados com sucesso."
    else:
        return f'Requisição falhou com o código de status: {response.status_code}'

def addBasicData(documentOfTime, pedido, vendedorName, clientName):
    totalVenda = float(pedido['Total'])


    if not clientName in documentOfTime['clientesDb']:
        documentOfTime['clientesDb'][clientName] = createBasicClient(vendedorName, totalVenda)
    else:
        if vendedorName in documentOfTime['clientesDb'][clientName]['absoluteValues']:
            documentOfTime['clientesDb'][clientName]['absoluteValues'][vendedorName] += totalVenda
        else:
            documentOfTime['clientesDb'][clientName]['absoluteValues'][vendedorName] = totalVenda


    if vendedorName not in documentOfTime:
        #create vendedor
        documentOfTime[vendedorName] = {
            'totalVendido': totalVenda,
            'qtdVendas': 1,
            'qtdPortas': 0,
            'clientes': [clientName]
        }
        #update vendedor values
    else:
        documentOfTime[vendedorName]['totalVendido'] += totalVenda
        documentOfTime[vendedorName]['qtdVendas'] += 1
        if not clientName in documentOfTime[vendedorName]['clientes']:
            documentOfTime[vendedorName]['clientes'].append(clientName)



    return documentOfTime

def createBasicClient(vendedorName, totalVenda):
    return {
            'absoluteValues':{vendedorName:totalVenda},
            'porcentagemValues':{}
        }


def addPortaDados(documentOfTime, pedido, vendedorName):
    if 'Itens' in pedido:
        items = pedido['Itens']
        for item in items:
            if 'PORTA' in item['Nome']:
                documentOfTime[vendedorName]['qtdPortas'] += int(item['Qtde'])
    return documentOfTime


def addPercentageCliente(documentOfTime):


    for clientKey, clientData in documentOfTime['clientesDb'].items():
        # import ipdb; ipdb.set_trace()
        absolute_values = clientData['absoluteValues']
        total_value = sum(absolute_values.values())
    
        percentage_values = {}

        for seller, value in absolute_values.items():
                percentage = (value / total_value) * 100
                percentage_values[seller] = round(percentage, 2)  # Arredonda para 2 casas decimais
        
        documentOfTime['clientesDb'][clientKey]['percentageValues'] = percentage_values

    return documentOfTime

def generate_ranking(data):
    # Criar listas separadas para os diferentes critérios de classificação
    ranking_vendedor = []
    ranking_porteiro = []
    ranking_valor = []
    ranking_cliente = []

    for vendedor, datas in data.items():
        if vendedor == "data" or vendedor == "pedidosId" or vendedor == "clientesDb":
            continue
        # import ipdb; ipdb.set_trace()
        
        ranking_vendedor.append((vendedor, datas["qtdVendas"]))
        ranking_porteiro.append((vendedor, datas["qtdPortas"]))
        ranking_valor.append((vendedor, datas["totalVendido"]))
        ranking_cliente.append((vendedor, len(datas["clientes"])))

    # Ordenar as listas de acordo com os diferentes critérios
    ranking_vendedor.sort(key=lambda x: x[1], reverse=True)
    ranking_porteiro.sort(key=lambda x: x[1], reverse=True)
    ranking_valor.sort(key=lambda x: x[1], reverse=True)
    ranking_cliente.sort(key=lambda x: x[1], reverse=True)

    # Adicionar rankings ao documento
    rank = 1
    for vendedor, _ in ranking_vendedor:
        data[vendedor]["rank_vendedor"] = rank
        rank += 1
    rank = 1
    for vendedor, _ in ranking_porteiro:
        data[vendedor]["rank_porteiro"] = rank
        rank += 1

    rank = 1
    for vendedor, _ in ranking_valor:
        data[vendedor]["rank_value"] = rank
        rank += 1

    for vendedor, _ in ranking_cliente:
        data[vendedor]["rank_cliente"] = rank
        rank += 1

    return data

# Exemplo de uso:
if __name__ == "__main__":
    base_url = 'https://sistema.wvetro.com.br/wvetro/rest/api/'
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJVc2VyIjoibWF0aGV1cyBmbG9yZW50aW5vIGRlIGNhcnZhbGhvIiwiTGljZW5zZSI6IjI0NzkiLCJleHAiOjE2OTk0NzMyMDIsImlhdCI6MTY5OTQ3MzIwMiwianRpIjoiYmUwZTM3ZmMtMjQ0MC00YTFkLWI4NjktYjM1YmIxZTM0MjlhIiwiUGFzc3dvcmQiOiIxMjM0NTYifQ.NMf6vNrMf100hhClbO_2pfLKWWAvuWLqI0spWtGE4Js'
    headers = {'token': token}
    MONGO_URI = "mongodb+srv://matheusfcarvalho2001:3648@cluster0.rioem39.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(MONGO_URI)
    client = client['pequi']
    db = client['vendedores']
    reset = True

    result = get_current_month_data(base_url, headers, db, reset)
    print(result)
