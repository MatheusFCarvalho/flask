from typing import Iterable

class Vendas():
    def __init__(self, mes: str, valorTotal:float, qtdVendas: int, portas: int ):
        self.mes = mes
        self.valorTotal = valorTotal
        self.qtdvendas = qtdVendas
        self.portas = portas
        self.pedidosId

class Vendedor:
    def __init__(self, nome: str, vendasTotal: Iterable[Vendas], clientes):
        self.nome = nome
        self.vendasTotal = vendasTotal
        self.clientes = clientes        

    def adicionarVenda():
        
        pass

class ValorComprado():
    def __init__(self, mes:str, valor:float):
        self.mes = mes
        self.valor = valor

class Cliente:
    def __init__(self, nome:str, vendedoresId: Iterable[str], valoresComprado: Iterable[ValorComprado]):
        self.nome = nome
        self.vendedoresId = vendedoresId 
        self.valoresComprado = valoresComprado

    def atualizarValoresComprados(self):
        pass


class Pedidos():
    def __init__(self, id, data, valor:, vendedor, cliente)
        self.valor = valor 
        idWvetro: str
        vendedor: str
        qtdPorta: int
        cliente: str
