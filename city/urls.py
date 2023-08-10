from django.urls import path
from .views import *

app_name = 'city'

urlpatterns = [
    path('list/', CityListView.as_view(), name='city_list'),
    path('detail/<int:content_id>/', CityDetailView.as_view(), name='city_detail'),
]