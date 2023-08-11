from django.urls import path
from .views import *

app_name = 'city'

urlpatterns = [
    path('list/', CityTravelListView.as_view(), name='city_list'),
    #test url = 127.0.0.1:8000/city/list/?area_code=35
    path('fest/', CityFestListView.as_view(), name='city_fest_list'),
    path('total/', CityTotal2ListView.as_view(), name='city_tlist'),
    path('detail/<int:content_id>/', CityDetailView.as_view(), name='city_detail'),
]