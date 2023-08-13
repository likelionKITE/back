from django.urls import path
from .views import *

app_name = 'travel'

urlpatterns = [
    path('list/', TravelListView.as_view(), name='travel_list'),
    #test url = 127.0.0.1:8000/travel/list/?cat1=A02&cat2=A0201
    path('detail/<int:content_id>/', TravelDetailView.as_view(), name='travel_detail'),
    path('like/<int:content_id>/', like, name='travel_like'),
    path('review/<int:content_id>/', ReviewListView.as_view(), name='travel_review'),
]