from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category
from .utilities import getColor, numOfChildren, incrementID, getNLevelChildren, categoryDetails, update
import simplejson as json

# Index view that returns all the categories


@api_view(['GET'])
def index(request):
    categories = Category.objects.all()

    res = {
        "categories": []
    }

    for category in categories:
        details = categoryDetails(category)
        res["categories"].append(details)

    return HttpResponse(json.dumps(res, use_decimal=True), content_type="application/json")

# View to create a category and return the details of the new category


@api_view(['POST'])
@csrf_exempt
def createCategory(request):
    body = request.data
    categoryName = body["categoryName"]
    categoryParentID = body["categoryParentID"]
    targetSales = body["targetSales"]
    currentSales = body["currentSales"]
    progressPercentage = round(int(currentSales) / int(targetSales), 2)
    progressColor = getColor(progressPercentage)

    if categoryParentID:
        parent = Category.objects.get(categoryID=categoryParentID)
        numOfSiblings = numOfChildren(parent)
    else:
        parent = None

    categoryID = body["categoryID"] or (
        categoryName + ' ' + incrementID(numOfSiblings))

    newCategory = Category(categoryName=categoryName,
                           categoryID=categoryID,
                           targetSales=targetSales,
                           currentSales=currentSales,
                           progressPercentage=progressPercentage,
                           progressColor=progressColor,
                           parent=parent)
    newCategory.save()

    res = categoryDetails(newCategory)

    return HttpResponse(json.dumps(res, use_decimal=True), content_type="application/json")

# View to update the details of a category


@api_view(['PUT'])
@csrf_exempt
def updateCategory(request):
    body = request.data

    categoryID = body["categoryID"]
    targetSalesNew = body["targetSales"]
    currentSalesNew = body["currentSales"]

    updatedCategory = Category.objects.get(categoryID=categoryID)

    targetSalesOld = updatedCategory.targetSales
    currentSalesOld = updatedCategory.currentSales

    update(updatedCategory, targetSalesOld, targetSalesNew,
           currentSalesOld, currentSalesNew)

    res = categoryDetails(updatedCategory)

    return HttpResponse(json.dumps(res, use_decimal=True), content_type="application/json")

# View to get a category and it's N level children


@api_view(['GET'])
def getCategoryAndChildren(request):
    categoryID = request.headers.get('Categoryid')
    numOfLevels = int(request.headers.get('Numoflevels'))

    res = {
        "categories": []
    }

    category = Category.objects.get(categoryID=categoryID)

    categories = [category]
    categories = getNLevelChildren(
        category, numOfLevels, categories)

    for category in categories:
        details = categoryDetails(category)
        res["categories"].append(details)

    return HttpResponse(json.dumps(res, use_decimal=True), content_type="application/json")

# View to get the parent of a category


@api_view(['GET'])
def getCategoryParents(request):
    categoryID = request.headers.get('Categoryid')
    category = Category.objects.get(categoryID=categoryID)

    if category.parent:
        res = categoryDetails(category.parent)
        return HttpResponse(json.dumps(res, use_decimal=True), content_type="application/json")
    else:
        return HttpResponse(json.dumps("No parent"), content_type="application/json")

# View to delete a category


@api_view(['DELETE'])
@csrf_exempt
def deleteCategory(request):
    categoryID = request.headers.get('Categoryid')
    deleteChildren = request.headers.get('Deletechildren', "False")

    category = Category.objects.get(categoryID=categoryID)

    if deleteChildren == "False":
        category.delete()
        return HttpResponse(json.dumps("Category deleted"), content_type="application/json")

    descendants = list(category.get_descendants(include_self=True))
    descendants.reverse()

    for descendant in descendants:
        descendant.delete()

    return HttpResponse(json.dumps("Category and descendants deleted"), content_type="application/json")
