from django.urls import path

from . import views


app_name = 'inpx'

urlpatterns = [
    path('statistic/', views.StatisticList.as_view(), name='statistic'),
    path('update/', views.DbUpdate.as_view(), name='update'),
    path('clear/', views.DbClear.as_view(), name='clear'),
]
