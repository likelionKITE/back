from django.urls import path

from member.views import MypageCombinedView, ChangeNicknameView

app_name = 'member'

urlpatterns = [
    path('mypage/', MypageCombinedView, name='mypage'),
    path('changenickname/', ChangeNicknameView.as_view(), name='changenickname'),
]