from django.urls import path
from .views import createCategory, updateCategory, getCategoryAndChildren, getCategoryParents, deleteCategory, index

urlpatterns = [
    path('', index, name='index'),
    path('create/', createCategory, name='createCategory'),
    path('update/', updateCategory, name='updateCategory'),
    path('getchildren/', getCategoryAndChildren, name='getCategoryAndChildren'),
    path('getparents/', getCategoryParents, name='getCategoryParents'),
    path('delete/', deleteCategory, name='deleteCategory'),
]
