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
