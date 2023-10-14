def verifyAllItemsIsDone(items):
    for item in items:
        if not 'isDone' in item:
            return False
        elif not item['isDone'] == True:
            return False
    return True

def verifyIfClientAlreadyExist(roteiro, pedido):
        boolzin = False
        for pedidoRota in roteiro['pedidos']:
            if pedidoRota['cliente'] == pedido['cliente']:
                pedidoRota['pedidos'].append(pedido['pedidos'][0])
                boolzin = True
        
        if boolzin == False:
            roteiro['pedidos'].append(pedido)
        
        return roteiro
