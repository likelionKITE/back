from django.urls import path
from .views import *
from main.views import ReviewListView, ReviewDetailView

app_name = 'festival'

urlpatterns = [
    path('list/', FestivalCombinedView_main, name='combined_view'),
    path('detail/<int:content_id>/', FestivalDetailView.as_view(), name='festival_detail'),
    path('search/', FestivalSearchView.as_view(), name='festival_search'),
    path('like/<int:content_id>/', like, name='festival_like'), ##### 복붙
    path('review/<int:content_id>/', ReviewListView.as_view(), name='festival_review'),
    path('review/detail/<int:content_id>/', ReviewDetailView.as_view(),name='festival_review_detail'),
]