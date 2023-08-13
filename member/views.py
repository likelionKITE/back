from django.shortcuts import render

from main.models import Tour, Review
from concurrent.futures import ThreadPoolExecutor
from django.http import JsonResponse
from main.serializers import MainReviewSerializer
from festival.serializers import FestivalSerializer

from main.serializers import ReviewWithTourSerializer

from member.models import CustomUser

from rest_framework import generics

from member.serializers import CustomUserSerializer

from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

# Create your views here.
class ChangeNicknameView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

@login_required(login_url='/member/login')
def user_like_view_logic(request):
    queryset = Tour.objects.filter(like_users=request.user)
    serializer = FestivalSerializer(queryset, many=True)
    return serializer.data

@login_required(login_url='/member/login')
def user_review_logic(request):
    queryset = Review.objects.filter(user=request.user)
    serializer = ReviewWithTourSerializer(queryset, many=True)
    return serializer.data


def MypageCombinedView(request):
    data = {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_view1 = executor.submit(user_like_view_logic, request)
        future_view2 = executor.submit(user_review_logic, request)

        data['nickname'] = request.user.nickname
        data['user_like_response'] = future_view1.result()
        data['user_review_response'] = future_view2.result()

    return JsonResponse(data)