import aiUtils

def getOutCategories(data, label):
    categories = []
    categories = fill(len(label), 0.00, categories)

    for i in range(len(data)):
        if data["Money Out"][i] > 0:
            matchCategory = aiUtils.match(data["Transaction Description"][i], label)
            index = search(matchCategory, label)

            categories[index] += data["Money Out"][i]

    return categories

def getInCategories(data, label):
    
    categories = []
    categories = fill(len(label), 0.00, categories)

    for i in range(len(data)):
        if data["Money In"][i] > 0:
            matchCategory = aiUtils.match(data["Transaction Description"][i], label)
            index = search(matchCategory, label)

            categories[index] += data["Money In"][i]

    return categories

def getEssentialsData(data, label):
    statistics = [0.00, 0.00]

    for x in range(len(data)):
        if(data["Money Out"][x] > 0):
            response = aiUtils.match(data["Transaction Description"][x], label)

            if response[0] == "e":
                statistics[0] += data["Money Out"][x]
            else:
                statistics[1] += data["Money Out"][x]

    return statistics
    

def fill(size, target, list):
    for i in range(size):
        list.append(target)

    return list

def search(target, items):
    found = -1
    for i in range(len(items)):
        if items[i] == target:
            found = i

    return found

def findMax(data):
    greatest = -1
    pos = -1

    for i in range(len(data)):
        if data[i] > greatest:
            greatest = data[i]
            pos = i

    return pos

def calculatePercentageChange(final, initial):
    result = ((final - initial) / initial) * 100

    return result.round(2)


