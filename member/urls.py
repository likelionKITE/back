from django.urls import path
from member import views

from member.views import MypageCombinedView, ChangeNicknameView

app_name = 'member'

urlpatterns = [
    path('mypage/', MypageCombinedView, name='mypage'),
    path('changenickname/', ChangeNicknameView.as_view(), name='changenickname'),
    path('google/login', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),  
   path('google/login/finish/', views.GoogleLogin.as_view(), name='google_login_todjango'),
]