from flask import render_template, Blueprint, request
from . import getDadosVendedoresFromDocumentoForAdmin, getMesesDisponiveis, getDateSlashed, vendedoresCollection 
from functions.generateRanking import updateRanking, generateSpecificRanking
import datetime
from flask import request, redirect, url_for
# from pymongo import MongoClient

sell_bp = Blueprint('sellers', __name__)

@sell_bp.route('/<nome>', methods=['GET', 'POST'])
@sell_bp.route('/<nome>/<isPacific>', methods=['GET', 'POST'])
def perfil_vendedor(nome, isPacific='pacifico'):
    # Obter o documento do banco de dados

    documento = vendedoresCollection.find_one({'data': getDateSlashed()})
    # try:
    clientesTotaisDoc = vendedoresCollection.find_one({'tipo':'clientesAtuais', 'vendedor':nome})
        # clientesTotais = clientesTotaisDoc['clientes']
    clientesTotais = clientesTotaisDoc.get('clientes', False)
    if clientesTotais == False:
        vendedoresCollection.insert_one({'tipo': 'clientesAtuais', 'vendedor': nome, 'clientes':[] })
        clientesTotais = []
    # except TypeError:

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
        clientesNaoAtendidos = [cliente for cliente in clientesTotais if cliente not in clientes]
        qtdClientesNaoAtendidos = len(clientesNaoAtendidos)
        # Passe os dados como um dicionário com as chaves correspondentes


        senha = request.form.get('senha')
        # if request.method == 'POST':
            # if senha == senhaSystem.get(nome):
        mesesDisponiveis, mesesData = getMesesDisponiveis(nome)
        today = datetime.date.today()
        daysLeft = 30 - int(today.day)
        
        frase = "De grão em grão de areia se faz uma chapa de vidro!"

        dados_vendedor = {
                    "isPacific":isPacific,
                    "nome": nome,
                    "totalVendido": totalVendidoFormatado,
                    "qtdVendas": vendedor.get("qtdVendas", 0),
                    "qtdPortas": vendedor.get("qtdPortas", 0),
                    "qtdClientes": qtdClient,
                    "clientesName": clientes,
                    "clientesNaoAtendidos": clientesNaoAtendidos,
                    "qtdClientesNaoAtendidos":qtdClientesNaoAtendidos,
                    "clientesDb": clientesDbOfSeller,
                    "rank_vendedor": vendedor.get("rank_vendedor", 0),
                    "rank_porteiro": vendedor.get("rank_porteiro", 0),
                    "rank_value": vendedor.get("rank_value", 0),
                    "rank_cliente": vendedor.get("rank_cliente", 0),
                    "frase": frase,
                    "senha": senha, 
                    "updateInfo": updateInfo,
                    "mesesDisponiveis": mesesDisponiveis,
                    "daysLeft":daysLeft
                    # "mesesData": mesesData,
                }

        return render_template('perfil_vendedor.html', mesesData = mesesData, **dados_vendedor)
    else:
        # Se o vendedor não for encontrado, você pode lidar com isso de acordo com sua lógica, como exibir uma mensagem de erro.
        return "Vendedor não encontrado", 404
    


@sell_bp.route('/admin', methods=['GET'])
@sell_bp.route('/admin/<int:year>/<int:month>', methods=['GET'])
def admin(year=None, month=None):
    if year is None or month is None:
        formated_date = getDateSlashed()
    else:
        formated_date = f"{year:04d}/{month:02d}"

    

    documento = vendedoresCollection.find_one({"data": formated_date})
    dados_vendedores = getDadosVendedoresFromDocumentoForAdmin(documento)
    updateInfo = {'lastUpdate':documento['lastUpdate'], 'updatedBy': documento['updatedBy']}
                
    return render_template('admin/index.html',updateInfo=updateInfo, dados_vendedores=dados_vendedores)
    # return render_template('admin.html',updateInfo=updateInfo, dados_vendedores=dados_vendedores)

@sell_bp.route('/<nome>/atualizar_sistema', methods=['POST', 'GET'])
def atualizar_sistema(nome):


    
    # Adicione aqui a lógica de atualização do sistema usando a função updateRanking()
    updateRanking(nome)
    if nome == 'admin':
        return redirect(url_for('sellers.admin'))
    # Redirecione de volta ao perfil do vendedor após a atualização
    return redirect(url_for('sellers.perfil_vendedor', nome=nome, isPacific='competitivo'))

@sell_bp.route('/<nome>/atualizar_sistema_reset', methods=['POST', 'GET'])
def atualizar_sistema_reset(nome):
    # Adicione aqui a lógica de atualização do sistema usando a função updateRanking()
    updateRanking(nome, reset=True)

    if nome == 'admin':
        return redirect(url_for('sellers.admin'))
    # Redirecione de volta ao perfil do vendedor após a atualização
    return redirect(url_for('sellers.perfil_vendedor', nome=nome))

@sell_bp.route('/<nome>/atualizar_sistema/specific/<year>/<month>', methods=['POST'])
def generate_specific_ranking(nome, year, month):
    # Adicione aqui a lógica de atualização do sistema usando a função updateRanking()
    generateSpecificRanking(nome= nome, year=year, month=month)

    # Redirecione de volta ao perfil do vendedor após a atualização
    return redirect(url_for('sellers.perfil_vendedor', nome=nome))
