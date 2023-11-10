# from flask import render_template, Blueprint, request
# from pymongo import MongoClient

# bp = Blueprint('sellers', __name__)
# MONGO_URI = "mongodb+srv://matheusfcarvalho2001:3648@cluster0.rioem39.mongodb.net/?retryWrites=true&w=majority"

# @bp.route('/<nome>', methods=['GET'])
# def perfil_vendedor(nome):
#     # Conectar ao banco de dados MongoDB
#     client = MongoClient(MONGO_URI)
#     db = client['pequi']
#     vendedores_collection = db['vendedores']

#     # Obter o documento do banco de dados
#     documento = vendedores_collection.find_one({})

#     if documento and nome in documento:
#         # Se o nome do vendedor existe no documento, pegue os dados desse vendedor
#         vendedor = documento[nome]
#         return render_template('perfil_vendedor.html', vendedor=vendedor)
#     else:
#         # Se o vendedor não for encontrado, você pode lidar com isso de acordo com sua lógica, como exibir uma mensagem de erro.
#         return "Vendedor não encontrado", 404
from functions.generateRanking import updateRanking
from flask import render_template, Blueprint, request
from pymongo import MongoClient

bp = Blueprint('sellers', __name__)
MONGO_URI = "mongodb+srv://matheusfcarvalho2001:3648@cluster0.rioem39.mongodb.net/?retryWrites=true&w=majority"

@bp.route('/<nome>', methods=['GET', 'POST'])
def perfil_vendedor(nome):
    # Conectar ao banco de dados MongoDB
    client = MongoClient(MONGO_URI)
    db = client['pequi']
    vendedores_collection = db['vendedores']
    # Obter o documento do banco de dados
    documento = vendedores_collection.find_one({})


    if documento and nome in documento:
        # Se o nome do vendedor existe no documento, pegue os dados desse vendedor
        vendedor = documento[nome]
        updateInfo = {'lastUpdate':documento['lastUpdate'], 'updatedBy': documento['updatedBy']}
        # Formate o valor totalVendido como moeda com 2 casas decimais e o símbolo "R$"
        totalVendidoFormatado = f'R$ {vendedor.get("totalVendido", 0):,.2f}'
        clientes = vendedor.get("clientes", [])
        clientesDb = documento.get("clientesDb", {})
        qtdClient = len(clientes)
        
        clientesDbOfSeller = {cliente: clientesDb.get(cliente) for cliente in clientes}
        
        # Passe os dados como um dicionário com as chaves correspondentes
        senhaSystem = {
            'michelle boschetti':'golden',
            'beatriz boschetti':'senhora',
            'bianca boschetti':'',
            'fernando boschetti':'golf',
            'valter souza':'esfola',
            'willian souza':'sistema', 
            'luciana rocha':'fua',
            'tatiane brockyeld':'cocacola',

        }

        fraseSystem = {
            'michelle boschetti':'calma na alma que passa',
            'beatriz boschetti':'obrigado meu Deus pelo cafézinho de cada dia',
            'bianca boschetti':'assina aqui por favor',
            'fernando boschetti':'golfão gti: https://www.youtube.com/watch?v=AA3__qlakw4',
            'valter souza':'surf na praia é bom d++',
            'willian souza':'sistema novo?', 
            'luciana rocha':'cuidado com o fuá',
            'tatiane brockyeld':'hmmm coquinha gelada bom d++++',
        }

        senha = request.form.get('senha')
        # if request.method == 'POST':
            # if senha == senhaSystem.get(nome):
        dados_vendedor = {
                    "nome": nome,
                    "senhaSystem": senhaSystem,
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
                    "frase": fraseSystem[nome],
                    "senha": senha, 
                    "updateInfo": updateInfo,
                }
        #     else:
        #         # Se a senha estiver incorreta, passe apenas o nome e a senha
        #         dados_vendedor = {"nome": nome, "senha": "", "acesso_negado": True, "senhaSystem": senhaSystem}
        # else:
        #     # Se não for uma solicitação POST, passe apenas o nom
        #     dados_vendedor = {"nome": nome, "senha": "","senhaSystem": senhaSystem }
        return render_template('perfil_vendedor.html', **dados_vendedor)
    else:
        # Se o vendedor não for encontrado, você pode lidar com isso de acordo com sua lógica, como exibir uma mensagem de erro.
        return "Vendedor não encontrado", 404

@bp.route('/admin', methods=['GET'])
def admin():
    # Conectar ao banco de dados MongoDB
    client = MongoClient(MONGO_URI)
    db = client['pequi']
    vendedores_collection = db['vendedores']

    # Obtenha todos os documentos de vendedores
    documentos = vendedores_collection.find()

    # Crie uma lista para armazenar os dados de todos os vendedores
    dados_vendedores = []

    for documento in documentos:
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
    # Passe a lista de dados_vendedores para o template de administração
    return render_template('admin.html', dados_vendedores=dados_vendedores)


from flask import request, redirect, url_for

# ...
@bp.route('/<nome>/atualizar_sistema', methods=['POST'])
def atualizar_sistema(nome):
    # Adicione aqui a lógica de atualização do sistema usando a função updateRanking()
    updateRanking(nome)

    # Redirecione de volta ao perfil do vendedor após a atualização
    return redirect(url_for('sellers.perfil_vendedor', nome=nome))