from django.urls import path

from client.views import ClientList, ClientCreate, ClientUpdate, ClientDetail

app_name = "client"

urlpatterns = [
    path('salon/<int:salon_id>', ClientList.as_view(), name="list"),
    path('new/', ClientCreate.as_view(), name="new"),
    path('<int:pk>/', ClientDetail.as_view(), name="detail"),
    path('update/<int:pk>/', ClientUpdate.as_view(), name="update"),
]
