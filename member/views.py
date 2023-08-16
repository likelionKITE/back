from django.shortcuts import render
from main.models import Tour, Review
from main.serializers import ReviewWithTourSerializer
from concurrent.futures import ThreadPoolExecutor
from django.http import JsonResponse
from festival.serializers import FestivalSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import generics
from member.models import CustomUser
from rest_framework import status
from rest_framework.response import Response

from member.serializers import CustomUserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required


# Create your views here.
class ChangeNicknameView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        return self.request.user

# @login_required(login_url='/member/login/')
def user_like_view_logic(request):
    queryset = Tour.objects.filter(like_users=request.user)
    serializer = FestivalSerializer(queryset, many=True)
    return serializer.data

# @login_required(login_url='/member/login/')
def user_review_logic(request):
    queryset = Review.objects.filter(user=request.user)
    serializer = ReviewWithTourSerializer(queryset, many=True)
    return serializer.data

# @login_required(login_url='/member/login')
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def MypageCombinedView(request):
    data = {}
    if not request.user.is_authenticated:
        return Response({"message": "로그인한 사용자만 접근할 수 있습니다."}, status=status.HTTP_401_UNAUTHORIZED)
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_view1 = executor.submit(user_like_view_logic, request)
        future_view2 = executor.submit(user_review_logic, request)

        data['nickname'] = request.user.nickname
        data['user_like_response'] = future_view1.result()
        data['user_review_response'] = future_view2.result()

    return JsonResponse(data)