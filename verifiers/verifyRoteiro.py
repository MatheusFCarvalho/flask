def verifyAllItemsIsDone(items):
    for item in items:
        if not 'isDone' in item:
            return False
        elif not item['isDone'] == True:
            return False
    return True
def verifyIfCanAddRequest(pedido, number):
    if number in pedido['pedidos'] and number not in pedido['pedidosFeito']:
        return True
    return False

def verifyAllItemsIsDoneExcel(pedido):
    pedidos = pedido['pedidos']
    pedidosFeito = pedido['pedidosFeito']
    if len(pedidos) == len(pedidosFeito):
        for pedid in pedidos:
            if not pedid in pedidosFeito:
                return False
        for pedid in pedidosFeito:
            if not pedid in pedidos:
                return False
        return True
    return False

def verifyIfClientAlreadyExist(roteiro, pedido):
        boolzin = False
        for pedidoRota in roteiro['pedidos']:
            if pedidoRota['cliente'] == pedido['cliente']:
                pedidoRota['pedidos'].append(pedido['pedidos'][0])
                boolzin = True
        
        if boolzin == False:
            roteiro['pedidos'].append(pedido)
        
        return roteiro

def verifyIfExcelAreRight(roteiro):
    isError = False
    import ipdb;
    ipdb.set_trace()
    lines = roteiro.split('\n')[2:]
    for line in lines:
        datas = line.split('\t')
        if not datas[1].isnumeric():
            isError = True
    # print(rotei)
    return isError
    
