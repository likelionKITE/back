from django.urls import path
from .views import *
from main.views import ReviewListView, ReviewDetailView

app_name = 'city'

urlpatterns = [
    # path('list/', CityTravelListView.as_view(), name='city_list'),
    #test url = 127.0.0.1:8000/city/list/?area_code=35
    # path('fest/', CityFestListView.as_view(), name='city_fest_list'),
    path('list/', CityTotalListView.as_view(), name='city_tlist'),
    path('detail/<int:content_id>/', CityDetailView.as_view(), name='city_detail'),
    path('like/<int:content_id>/', like, name='city_like'),
    path('review/<int:content_id>/', ReviewListView.as_view(), name='city_review'),
    path('review/detail/<int:content_id>/', ReviewDetailView.as_view(), name='city_review_detail'),
]