def verifyAllItemsIsDone(items):
    for item in items:
        if not 'isDone' in item:
            return False
        elif not item['isDone'] == True:
            return False
    return True