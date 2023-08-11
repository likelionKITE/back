from django.urls import path
from .views import *

app_name = 'festival'

urlpatterns = [
    path('list/', FestivalCombinedView_main, name='combined_view'),
]