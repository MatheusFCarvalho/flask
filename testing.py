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
ENTREGAS 10-10 --- ZONA LESTE + ZONA SUL					
CLIENTE 	PEDIDO	PEÇAS	SEPARADOR	ENDEREÇO 	OBS:
IN VITRO 	22950	2		RUA MARIA APARECIDA CARMO SILVA - 25 	LIBERADO
	22977	5			
TIAGO SANTA MARIA 	22941	1		COLOCAR ENDEREÇO NO SISTEMA 	LIBERADO
	22898	2			
WA MOVELARIA 	22961	2		COLOCAR ENDEREÇO NO SISTEMA 	LIBERADO
ELITE DO AQUARIO 	22985	4		RUA DJANIRA DE PAULA FREIRE - 209 	RECEBER 92,83
PLANEJ MOVELARIA 	22900	1		RUA CARAVELAS - 426	LIBERADO
TOP VALE VIDROS 	22979	2		RUA ITABAIANA - 458 PQ INDUSTRIAL 	RECEBER 262,43
PEDRO PINTURA 	22647	1		DEIXAR VIDRO TEMPERADO DA SOFISTICASA / VIDRO CHEGA HOJE 09-10	...
ARTHOME	21722	2		RUA JOSEFA ALBUQUERQUE DOS SANTOS - 958 JD MORUMBI 	RECEBER 555,00
TOTAL : 	10	22			
"""

mongodb_doc = parse_text_to_mongodb_doc(text)
print(mongodb_doc)
