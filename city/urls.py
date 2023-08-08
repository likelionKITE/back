from django.urls import path
from .views import *

app_name = 'movie'

urlpatterns = [
    path('list/', CityListView.as_view(), name='city_list'),
]