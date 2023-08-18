from django.shortcuts import render
from main.models import ServiceCode, AreaCode, Tour, DetailInfo, DetailCommon, Review
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import serializers
from .serializers import CitySerializer
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.response import Response

from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# Create your views here.
class CustomCitySerializer(CitySerializer):
            sido_part = serializers.SerializerMethodField()
            sigungu_part = serializers.SerializerMethodField()

            def get_sido_part(self, obj):
                addr1 = obj.addr1
                parts = addr1.split(',')
                return parts[-1].strip() if parts else ''

            def get_sigungu_part(self, obj):
                addr1 = obj.addr1
                parts = addr1.split(',')
                return parts[-2].strip() if len(parts) >= 2 else ''

            class Meta(CitySerializer.Meta):
                fields = ('title', 'first_image', 'sido_part', 'sigungu_part', 'content_id', 'content_type_id')

# class CityPagination(LimitOffsetPagination):
#     default_limit = 20
#===================================================================================================

# class CityTravelListView(generics.ListAPIView):
#     serializer_class = CustomCitySerializer
#     pagination_class = CityPagination
#
#     def get_queryset(self):
#         area_selected = self.request.GET.get('area_code')
#         queryset = Tour.objects.filter(content_type_id="76")  # 해당 지역의 여행지 데이터 가져오기
#         if area_selected:
#             queryset = queryset.filter(area_code=area_selected)
#         return queryset
#
# class CityFestListView(generics.ListAPIView):
#     serializer_class = CustomCitySerializer
#     pagination_class = CityPagination
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#
#     def get_queryset(self):
#         area_selected = self.request.GET.get('area_code')
#         current_month = datetime.today().strftime("%Y%m")
#
#         queryset = Tour.objects.filter(content_type_id="85")  # 해당 지역의 축제 데이터 가져오기
#         if area_selected:
#             queryset = queryset.filter(area_code=area_selected)
#
#         queryset = queryset.filter(
#             Q(detail_intro_fest__event_start_date__contains=current_month) |
#             Q(detail_intro_fest__event_end_date__contains=current_month)
#         )
#
#         return queryset

class CityDetailView(generics.RetrieveAPIView):
    serializer_class = CitySerializer


    def get_object(self):
        queryset = self.get_queryset()
        content_id = self.request.query_params.get('content_id')

        if content_id is not None:
            queryset = queryset.filter(content_id=content_id)

        obj = generics.get_object_or_404(queryset, content_id=self.kwargs['content_id'])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        return Tour.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance)

        like_user_exists = "False"
        if request.user.is_authenticated and instance.like_users.filter(id=request.user.id).exists():
            like_user_exists = "True"

        response_data = serializer.data
        response_data['like_user_exists'] = like_user_exists

        return Response(response_data)

class CityTotalListView(generics.ListAPIView):
    serializer_class = CustomCitySerializer


    def get_queryset(self):
        area_selected = self.request.GET.get('area_code')
        current_date = datetime.today().strftime("%Y%m%d")

        travel_queryset = Tour.objects.filter(content_type_id="76")
        fest_queryset = Tour.objects.filter(content_type_id="85")

        if area_selected:
            travel_queryset = travel_queryset.filter(area_code=area_selected)
            fest_queryset = fest_queryset.filter(area_code=area_selected)

        fest_queryset = fest_queryset.filter(
            Q(detail_intro_fest__event_start_date__lte=current_date) &
            Q(detail_intro_fest__event_end_date__gte=current_date)
        )

        total_queryset = travel_queryset.union(fest_queryset)
        return total_queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            travel_data = []
            fest_data = []

            for obj in serializer.data:
                if obj['content_type_id'] == '76':
                    travel_data.append(obj)
                elif obj['content_type_id'] == '85':
                    fest_data.append(obj)
            
            result = {
                'travel': travel_data,
                'fest': fest_data
            }

            return self.get_paginated_response(result)
        
        serializer = self.get_serializer(queryset, many=True)
        travel_data = []
        fest_data = []

        for obj in serializer.data:
            if obj['content_type_id'] == '76':
                travel_data.append(obj)
            elif obj['content_type_id'] == '85':
                fest_data.append(obj)

        area_dict = {}
        for i in AreaCode.objects.all():
            if i.name not in area_dict:
                area_dict[i.name] = i.code

        result = {
            'travel': travel_data,
            'fest': fest_data,
            'area_dict': area_dict
        }

        return Response(result)


########################################### LIKE ###########################################
# @login_required(login_url='/member/login')
@api_view(['POST', 'GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def like(request,content_id):
    if request.method == 'POST':
        # 어떤 게시물에, 어떤 사람이 like를 했는 지
        tour = Tour.objects.get(content_id=content_id) # 게시물 번호 몇번인지 정보 가져옴
        user = request.user
        if not request.user.is_authenticated:
            return JsonResponse({"message": "로그인한 사용자만 접근할 수 있습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        if tour.like_users.filter(id=request.user.id).exists(): # 유저면 알아서 유저의 id로 검색해줌
            tour.like_users.remove(user)
            return JsonResponse({'message': 'deleted', 'like_cnt' : tour.like_users.count() })
        else:
            tour.like_users.add(user) # post의 like에 현재유저의 정보를 넘김
            return JsonResponse({'message': 'added', 'like_cnt' : tour.like_users.count()})
    if request.method == 'GET':
        tour = Tour.objects.get(content_id=content_id)  # 게시물 번호 몇번인지 정보 가져옴
        return JsonResponse({'like_cnt' : tour.like_users.count()})