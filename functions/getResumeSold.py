import requests
# import pandas as pd

base_url = 'https://sistema.wvetro.com.br/wvetro/rest/api/'

def getTokenWvetro():
    url ='https://sistema.wvetro.com.br/wvetro/rest/api/Integracao/ValidarUsuario?Licencaid=2479&Secusername=Matheus Florentino de Carvalho&Secuserpassword=123456'
    response = requests.get(url)
    responseData = response.json()
    return responseData['ValidaUsuario']['token']

token = getTokenWvetro()

headers = {'token': token}

from collections import defaultdict


['3MM', '4MM', '5MM', '6MM', '8MM', '10MM', '3+3', '4+4', '5+5']

class Manager:
    def __init__(self):
        self.especificaCores = defaultdict(float)
        self.especificaLap = defaultdict(float)
        self.especificaBis = defaultdict(float)
        self.metrolapidado = 0
        self.metrobisote = 0
        self.metrocortado = 0
        self.metrotemperado = 0
        self.redondoexterno = 0
        self.medidas_por_mm = {
            '3MM': 0,
            '4MM': 0,
            '5MM': 0,
            '6MM': 0,
            '8MM': 0,
            '10MM': 0,
            '3+3': 0,
            '4+4': 0,
            '5+5': 0
        }

    def totalMetroQuadrado(self):
        total = 0
        for cor, valor in self.especificaCores.items(): 
            total += valor
        return total


    def saveCut(self, item):
        id = item['Nro']
        if 'Itens' in item:
            for glasses in item['Itens']:
                if 'Vidros' in glasses:
                    for glass in glasses['Vidros']:
                        cor = glass['Especificacao']

                        newCorNome = cor
                        metroquadrado = float(glass['M2'])

                        if not 'TEMPERADO' in glasses['Nome'] and not 'TEMPERADO' in cor:  
                            if 'LAPIDADO' in glasses['Nome'] or 'LAPIDADO' in cor:

                                self.metrolapidado += metroquadrado
                            elif 'BISOTE' in glasses['Nome'] or 'BISOTE' in cor:
                                if 'REDONDO' in glasses['Nome'] or 'REDONDO' in cor:
                                    self.redondoexterno += metroquadrado
                                else:
                                    self.metrobisote += metroquadrado
                            else:
                                self.metrocortado += metroquadrado
                        else:
                            self.metrotemperado += metroquadrado
                            cor = glass['Especificacao']
                        mm_sizes = ['3MM', '4MM', '5MM', '6MM', '8MM', '10MM', '3+3', '4+4', '5+5']

                        for size in mm_sizes:
                            if size in cor:
                                self.medidas_por_mm[size] += float(metroquadrado)

    def resume(self, mes):
        cortado = int(self.metrocortado)
        lapidado = int(self.metrolapidado)
        bisote = int(self.metrobisote)
        temperado = int(self.metrotemperado)
        redondo = int(self.redondoexterno)
        message = f'Mês: {mes} - cortado: {cortado} - lapidado: {lapidado} - bisote: {bisote} - temperado: {temperado} - redondo externo: {redondo}'
        print(message)
        # print(self.medidas_por_mm)
        return message 

                        # self.especificaCores[newCorNome] += float(metroquadrado)
    # def exportToExcel(self, file_name):
    #     # Criando um DataFrame do pandas a partir do dicionário específicoCores
    #     df = pd.DataFrame(list(self.especificaCores.items()), columns=['Cor', 'Metros Quadrados'])
    #     df = df.sort_values(by='Metros Quadrados', ascending=False)
    #     # Escrevendo o DataFrame em um arquivo Excel
    #     df.to_excel(file_name, index=False)



year = '2023'
# formatted_month = '12'

formatted_months = ['6', '7', '8', '9', '10', '11', '12']


for formatted_month in formatted_months:
    manajo = Manager()
    url = f'{base_url}Pedidos/ListPedidos?Dtvendainicial={year}-{formatted_month}-01&Dtvendafinal={year}-{formatted_month}-31'

    response = requests.get(url, headers = headers)

    if response.status_code == 200:
        data = response.json()
        allPedidos = data['ListPedidos']
        for pedido in allPedidos:
            manajo.saveCut(pedido)
        # print(formatted_month)
        manajo.resume(formatted_month)

        # manajo.exportToExcel('mes9.xlsx')
        # print(f'lap: {manajo.metrolapidado}')
        # print(f'bis: {manajo.metrobisote}')
        # import ipdb; ipdb.set_trace()

print('finale')
