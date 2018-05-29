from django.urls import path

from staffer.views import (StafferCreate, StafferList, StafferUpdate, PositionView,
                           StafferInfoCreate, StafferDeleteService, PositionUpdate, PositionDelete, StafferDelete)

app_name = "staffer"

urlpatterns = [
    path('', StafferList.as_view(), name="list"),
    path('new/', StafferCreate.as_view(), name="new"),
    path('info/', StafferInfoCreate.as_view(), name="info"),
    path('<int:pk>/', StafferUpdate.as_view(), name="detail"),
    path('positions/', PositionView.as_view(), name="position"),
    path('service/delete/<int:pk>', StafferDeleteService.as_view(), name="del-service"),
    path('positions/<int:pk>', PositionUpdate.as_view(), name="position-update"),
    path('positions/delete/<int:pk>', PositionDelete.as_view(), name="position-delete"),
    path('delete/<int:pk>', StafferDelete.as_view(), name="delete")
]
