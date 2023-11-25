class Vendor:
    def __init__(self, name):
        self.name = name
        self.total_sold = 0
        self.sales_count = 0
        self.door_count = 0
        self.clients = []

    def add_sale(self, amount):
        self.total_sold += amount
        self.sales_count += 1

    def add_door(self, quantity):
        self.door_count += quantity

    def add_client(self, client_name):
        if client_name not in self.clients:
            self.clients.append(client_name)
            
    def __repr__(self):
        return (
            f"Vendor: {self.name}\n"
            f"Total Sold: {self.total_sold}\n"
            f"Number of Sales: {self.sales_count}\n"
            f"Number of Doors Sold: {self.door_count}\n"
            f"Clients: {', '.join(self.clients)}\n"
        )

class ReportGenerator:
    def __init__(self):
        self.vendors = {}
        self.pedidosId = []

    def process_single_pedido(self, pedido):
        nro_pedido = pedido['Nro']
        client_name = pedido['ClienteNome']
        vendor_name = pedido['VendedorNome'].lower()

        if vendor_name not in self.vendors:
            self.vendors[vendor_name] = Vendor(vendor_name)

        if nro_pedido not in self['pedidosId']:
            self.vendors[vendor_name].add_sale(float(pedido['Total']))
            self.vendors[vendor_name].add_client(client_name)

            if 'Itens' in pedido:
                items = pedido['Itens']
                for item in items:
                    if 'PORTA' in item['Nome']:
                        self.vendors[vendor_name].add_door(int(item['Qtde']))

    def generate_ranking(self):
        ranking_vendedor = []
        ranking_porteiro = []
        ranking_valor = []
        ranking_cliente = []
        ignoreFields = ['data', 'pedidosId', 'clientesDb', 'lastUpdate', 'updatedBy', '_id', 'rankings']


        for vendedor, vendedorData in self.vendors.items():
            if vendedor in ignoreFields:
                continue
            # import ipdb; ipdb.set_trace()
            
            ranking_vendedor.append((vendedor, vendedorData["qtdVendas"]))
            ranking_porteiro.append((vendedor, vendedorData["qtdPortas"]))
            ranking_valor.append((vendedor, vendedorData["totalVendido"]))
            ranking_cliente.append((vendedor, len(vendedorData["clientes"])))

        # Ordenar as listas de acordo com os diferentes critérios
        ranking_vendedor.sort(key=lambda x: x[1], reverse=True)
        ranking_porteiro.sort(key=lambda x: x[1], reverse=True)
        ranking_valor.sort(key=lambda x: x[1], reverse=True)
        ranking_cliente.sort(key=lambda x: x[1], reverse=True)

        rankings = {
            'rank_vendedor': ranking_vendedor,
            'rank_porteiro': ranking_porteiro,
            'rank_value': ranking_valor,
            'rank_cliente': ranking_cliente
        }
        self.rankings = rankings
        ranking_names = ['rank_vendedor', 'rank_porteiro', 'rank_value', 'rank_cliente']
        
        for rank_name in ranking_names:
            rank = 1
            for vendedor in rankings[rank_name]:
                self.vendors[vendedor][rank_name] = rank
                rank +=1

        # Your ranking generation logic here
        pass

    def process_all_pedidos(self, all_pedidos):
        for pedido in all_pedidos:
            self.process_single_pedido(pedido)

        self.generate_ranking()

    def __repr__(self):
        result = ""
        for vendor_name, vendor in self.vendors.items():
            result += f"{vendor}\n"
        return result

# Example usage
all_pedidos = [...]  # Assuming this is your list of pedidos
report_generator = ReportGenerator()
report_generator.process_all_pedidos(all_pedidos)
print(report_generator)  # This will print details for all vendors processed
