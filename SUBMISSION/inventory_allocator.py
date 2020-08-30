def inventoryAllocator(itemsNeeded, warehouses):
    '''Produces the cheapest shipment given items needed and warehouses available.
    Cheap warehouses are ordered from first, but priority is given to shipping from the
    least number of warehouses possible.

    Returns a list of dictionaries with warehouse names as keys, and items ordered from
    the warehouse as values. Items orderded is another dictionary with
    items as keys and quantities as values.

    Input arguments: a dictionary of items needed and a list of warehouses as dictionaries with
    keys of 'name' and 'inventory'.
    '''
    shipment = []
    for currentWarehouse in warehouses:
        itemsOrdered = {}
        itemsCompleted = []
        #add items that are currently needed
        for item in itemsNeeded:
            if item in currentWarehouse["inventory"]:
                quantityOrdered = min(currentWarehouse["inventory"][item], itemsNeeded[item])
                itemsOrdered[item] = quantityOrdered
                itemsNeeded[item] -= quantityOrdered
                currentWarehouse["inventory"][item] -= quantityOrdered
                if itemsNeeded[item] == 0:
                    itemsCompleted.append(item)
        for item in itemsCompleted:
            del itemsNeeded[item]
        #get the largest number of warehouses that can be combined with the current warehouse
        replaceableWarehouses = getReplaceableWarehousesRecursively(shipment, currentWarehouse, [], [])
        #if no items have been ordered from current warehouse, the warehouse must combine at least 2 previous warehouses to be used
        if itemsOrdered != {} or len(replaceableWarehouses) > 1:
            #combine past warehouse shipments into current warehouse
            for i in replaceableWarehouses:
                tupleWarehouseNameOrder = shipment[i].popitem()
                shipment.pop(i)
                for item, quantity in tupleWarehouseNameOrder[1].items():
                    if item in itemsOrdered:
                        itemsOrdered[item] += quantity
                    else:
                        itemsOrdered[item] = quantity
        if itemsOrdered != {}:
            shipment.append({currentWarehouse["name"]: itemsOrdered})
    #abandon order if items are still needed
    if len(itemsNeeded) > 0:
        return []
    return shipment


def getReplaceableWarehousesRecursively(shipment, currentWarehouse, maxIndexes, currentIndexes):
    '''Finds the greatest number of past orders that can be combined using the
    current warehouse. Iterates through the most expensive warehouses ordered
    from, and once a replaceable warehouse is found recursively calls function
    omitting the replaceable warehouse. Keeps track of the largest combination
    of orders that can be replaced.

    Returns a list of indexes for past orders in shipment.

    Input arguments: list of previous orders, current warehouse,
    list to hold the max replaceable indexes, and list to hold current
    replaceable indexes.
    '''
    #iterate through past orders from most expensive to cheapest
    for j in range(len(shipment) - 1, -1, -1):
        tupleWarehouseNameOrder = shipment[j].popitem()
        orderedItems = tupleWarehouseNameOrder[1]
        replaceable = True
        #determine if warehouse order can be replaced given current warehouse inventory
        for item, quantity in orderedItems.items():
            if item not in currentWarehouse["inventory"] or currentWarehouse["inventory"][item] < quantity:
                replaceable = False
                break
        #if replacable, change current warehouse inventory and recursively call function with shorter shipment list
        if replaceable:
            currentInventoryCopy = currentWarehouse["inventory"].copy()
            for item in orderedItems.keys():
                currentWarehouse["inventory"][item] -= orderedItems[item]
            currentIndexes.append(j)
            if len(currentIndexes) > len(maxIndexes):
                maxIndexes = currentIndexes.copy()
            maxIndexes = getReplaceableWarehousesRecursively(shipment[:j], currentWarehouse, maxIndexes, currentIndexes)
            #reset currentWarehouse inventory and current indexes
            currentWarehouse["inventory"] = currentInventoryCopy
            currentIndexes.pop()
        shipment[j][tupleWarehouseNameOrder[0]] = tupleWarehouseNameOrder[1]
    return maxIndexes
