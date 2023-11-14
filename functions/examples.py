import datetime


documentOfTimeInit = {
    'data': f'2023/11',
    'pedidosId': [],
    'clientesDb':{}
    }
    

exampleOfVendedor = {
    'totalVendido': 100,
    'qtdVendas': 1,
    'qtdPortas': 0,
    'clientes': ['clayto']
}

exampleOfClientesDb = {
    'japavidros':0
}

def getDateSlashed():
    today = datetime.date.today()
    year = today.year
    month = today.month
    formatted_month = f'{month:02d}'

    return f'{year}/{formatted_month}'



