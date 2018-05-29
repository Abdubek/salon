from django.urls import path

from timetable.views import TimeTableNew, TimeTableList, TimeTableMain

app_name = "timetable"

urlpatterns = [
    path('', TimeTableMain.as_view(), name="main"),
    path('<int:sid>', TimeTableNew.as_view(), name="new"),
    path('list/<int:sid>', TimeTableList.as_view(), name="list"),
]
