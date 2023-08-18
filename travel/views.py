from django.shortcuts import render
from main.models import ServiceCode, AreaCode, Tour, DetailInfo, DetailCommon, Review
from .models import DetailIntroTravel
from rest_framework import generics
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from .serializers import TravelSerializer
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework import status

# Create your views here.
class CustomTravelSerializer(TravelSerializer):
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

            class Meta(TravelSerializer.Meta):
                fields = ('title', 'first_image', 'sido_part', 'sigungu_part', 'content_id')

# class TravelPagination(LimitOffsetPagination):
#     default_limit = 20

#===================================================================================================

class TravelListView(generics.ListAPIView):
    # queryset = Tour.objects.filter(content_type_id="76")
    serializer_class = CustomTravelSerializer
    # pagination_class = TravelPagination

    def get_queryset(self):
        cat1_selected = self.request.GET.get('cat1')
        cat2_selected = self.request.GET.get('cat2')
        sort_method = self.request.GET.get('sortby')

        
        queryset = Tour.objects.filter(content_type_id="76")  # 여행지 데이터 가져오기
        
        if cat1_selected:
            queryset = queryset.filter(cat1=cat1_selected)
        
        if cat2_selected:
            queryset = queryset.filter(cat2=cat2_selected)

        if sort_method:
            queryset = queryset.annotate(count=Count('like_users')).order_by('-count')
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        travel_data = []

        serializer = self.get_serializer(queryset, many=True)

        for obj in serializer.data:
                travel_data.append(obj)

        main_sort = {}
        mid_sort = {}

        for i in ServiceCode.objects.all():
            main_name = i.main_name
            mid_name = i.mid_name
            mid_code = i.mid_code
            main_code = i.main_code
    
            if main_name not in mid_sort:
                mid_sort[main_name] = {}
    
            if main_name not in main_sort:
                main_sort[main_name] = main_code

            if main_name in mid_sort:
                mid_sort[main_name][mid_name] = mid_code

        result = {
            'travel_data': travel_data,
            'main_sort': main_sort,
            'mid_sort': mid_sort
            }
        
        return Response(result)

class TravelDetailView(generics.RetrieveAPIView):
    serializer_class = TravelSerializer

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