from django.urls import path
from .views import *

app_name = 'festival'

urlpatterns = [
    path('list/', FestivalCombinedView_main, name='combined_view'),
    path('detail/<int:content_id>/', FestivalDetailView.as_view(), name='festival_detail'),
    path('search/', FestivalSearchView.as_view(), name='festival_search'),
    path('like/<int:content_id>/', like, name='festival_like'), ##### 복붙
]