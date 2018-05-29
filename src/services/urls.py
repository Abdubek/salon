from django.urls import path

from services.views import (CategoryList, CategoryCreate, CategoryDetail, ServiceCreate,
                            SalonServices, ServiceUpdate, CategoryUpdate, CategoryDelete,
                            ServiceDelete)
from staffer.views import StafferAddService

app_name = "services"

urlpatterns = [
    path('', CategoryList.as_view(), name="list-category"),
    path('category/', CategoryCreate.as_view(), name="new-category"),
    path('category/<int:pk>', CategoryDetail.as_view(), name="category-detail"),
    path('category/update/<int:cid>', CategoryUpdate.as_view(), name="category-update"),
    path('category/delete/<int:pk>', CategoryDelete.as_view(), name="category-delete"),
    path('new/', ServiceCreate.as_view(), name="new"),
    path('salon/<int:sid>', SalonServices.as_view(), name="salon"),
    path('master', StafferAddService.as_view(), name="add-master"),
    path('update/<int:pk>', ServiceUpdate.as_view(), name="update"),
    path('delete/<int:pk>', ServiceDelete.as_view(), name="delete"),
]
