from pymongo import MongoClient


def getMesesDisponiveis(nome):
    MONGO_URI = "mongodb+srv://matheusfcarvalho2001:3648@cluster0.rioem39.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(MONGO_URI)
    db = client['pequi']
    vendedores_collection = db['vendedores']
    # Obter o documento do banco de dados
    documentos = vendedores_collection.find()
    mesesAvailable = []
    mesesData = {}
    for documento in documentos:
         if nome in documento:
            mesesAvailable.append(documento['data'])
            mesesData[documento['data']] = documento[nome]
    return mesesData, mesesData

def getDadosVendedoresFromDocumentoForAdmin(documento):
        dados_vendedores = []
        for nome, vendedor in documento.items():
            if isinstance(vendedor, dict):
                # Realize as operações de formatação de dados apenas para dicionários válidos
                totalVendidoFormatado = f'R$ {vendedor.get("totalVendido", 0):,.2f}'
                clientes = vendedor.get("clientes", [])
                clientesDb = documento.get("clientesDb", {})
                qtdClient = len(clientes)
                clientesDbOfSeller = {cliente: clientesDb.get(cliente) for cliente in clientes}

                # Crie um dicionário de dados_vendedor para este vendedor
                dados_vendedor = {
                    "nome": nome,
                    "totalVendido": totalVendidoFormatado,
                    "qtdVendas": vendedor.get("qtdVendas", 0),
                    "qtdPortas": vendedor.get("qtdPortas", 0),
                    "qtdClientes": qtdClient,
                    "clientesName": clientes,
                    "clientesDb": clientesDbOfSeller,
                    "rank_vendedor": vendedor.get("rank_vendedor", 0),
                    "rank_porteiro": vendedor.get("rank_porteiro", 0),
                    "rank_value": vendedor.get("rank_value", 0),
                    "rank_cliente": vendedor.get("rank_cliente", 0),
                }
                # Adicione o dicionário de dados_vendedor à lista de dados_vendedores
                dados_vendedores.append(dados_vendedor)
        dados_vendedores = sorted(dados_vendedores, key=lambda x: x['rank_value'], reverse=False)[1:]
        return dados_vendedores
