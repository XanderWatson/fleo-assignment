# Utility function to get the color of the progress bar from the percentage
def getColor(progressPercentage: float) -> str:
    if 0.00 <= progressPercentage <= 0.33:
        return "Red"
    elif 0.33 < progressPercentage <= 0.66:
        return "Yellow"
    else:
        return "Green"

# Utility function to increment the ID of a category


def incrementID(numOfSiblings: int) -> str:
    return chr(ord('A') + numOfSiblings)

# Utility function to get the number of children of a category


def numOfChildren(category) -> int:
    return len(category.children.all())

# Utility function to get the details of a category


def categoryDetails(category) -> dict:
    return {
        "categoryName": category.categoryName,
        "categoryID": category.categoryID,
        "targetSales": category.targetSales,
        "currentSales": category.currentSales,
        "progressPercentage": category.progressPercentage,
        "progressColor": category.progressColor,
    }

# Utility function to update the values of all the ancestor nodes of a category


def update(category, targetSalesOld, targetSalesNew, currentSalesOld, currentSalesNew) -> None:
    targetDiff = int(targetSalesNew) - int(targetSalesOld)
    currentDiff = int(currentSalesNew) - int(currentSalesOld)

    while category:
        category.targetSales += targetDiff
        category.currentSales += currentDiff
        category.progressPercentage = round(
            int(category.currentSales) / int(category.targetSales), 2)
        category.progressColor = getColor(category.progressPercentage)
        category.save()
        category = category.parent

# Utility function to get the children of N levels of a category


def getNLevelChildren(category, numOfLevels, categories) -> list:
    if numOfLevels == 0:
        return categories

    i = 0

    categs = [category.get_children()]
    subcategs = []

    while i < numOfLevels - 1:
        for categ in categs[i]:
            subcategs.extend(categ.get_children())
        categs.append(subcategs)
        i += 1

    for categ in categs:
        categories.extend(categ)

    return categories
