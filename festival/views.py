from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from django.db import models
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from rest_framework import generics
from main.models import Tour, AreaCode
from django.db.models import Q
from festival.serializers import FestivalSerializer, FestivalSerializer_now, FestivalDetailSerializer
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

# Create your views here.
def festival_list_view_logic(request):
    queryset = Tour.objects.filter(content_type_id="85").annotate(
        event_start_date=models.F('detail_intro_fest__event_start_date'))
    sort_method = request.GET.get('sortby')
    if sort_method == 'startdate':
        queryset = queryset.order_by('event_start_date')
    if sort_method == 'like':
        queryset = queryset.annotate(count=Count('like_users')).order_by('-count')


    serializer = FestivalSerializer(queryset, many=True)
    return serializer.data

def festival_now_view_logic():
    nowdate = datetime.today().strftime("%Y%m%d")
    queryset = Tour.objects.filter(content_type_id="85").annotate(
        event_start_date=models.F('detail_intro_fest__event_start_date'),
        event_end_date=models.F('detail_intro_fest__event_end_date')
    ).filter(event_start_date__lte=nowdate, event_end_date__gte=nowdate).order_by('?')[:11]
    serializer = FestivalSerializer_now(queryset, many=True)
    return serializer.data


class FestivalSearchView(generics.ListAPIView):

    serializer_class = FestivalSerializer

    def get_queryset(self):
        nowyear = datetime.today().strftime("%Y")
        month_selected = self.request.GET.get('month')
        area_selected = self.request.GET.get('area_code')
        sort_method = self.request.GET.get('sortby')

        queryset = Tour.objects.filter(content_type_id="85").annotate(
        event_start_date=models.F('detail_intro_fest__event_start_date'),
        event_end_date=models.F('detail_intro_fest__event_end_date')
    )  # 여행지 데이터 가져오기

        if month_selected:
            queryset = queryset.filter(Q(event_start_date__contains=nowyear+month_selected)|Q(event_end_date__contains=nowyear+month_selected))

        if area_selected:
            queryset = queryset.filter(area_code=area_selected)

        if sort_method == 'startdate':
            queryset = queryset.order_by('event_start_date')
        if sort_method == 'like':
            queryset = queryset.annotate(count=Count('like_users')).order_by('-count')

        return queryset


class FestivalDetailView(generics.RetrieveAPIView):
    serializer_class = FestivalDetailSerializer

    def get_object(self):
        content_id = self.request.query_params.get('content_id')
        queryset = Tour.objects.filter(content_type_id="85")

        if content_id is not None:
            queryset = queryset.filter(content_id=content_id)

        obj = generics.get_object_or_404(queryset, content_id=self.kwargs['content_id'])
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance)

        like_user_exists = "False"
        if request.user.is_authenticated and instance.like_users.filter(id=request.user.id).exists():
            like_user_exists = "True"

        response_data = serializer.data
        response_data['like_user_exists'] = like_user_exists

        return Response(response_data)

# 여러 뷰의 결과를 한 url에서 동시에 내보내기 - 근데 이렇게 하려면 view를 클래스형태가 아니라 저렇게 함수 형태로 구현해야 한대

@api_view(['GET'])
def FestivalCombinedView_main(request):
    data = {}
    if request.method == 'GET':
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_view1 = executor.submit(festival_list_view_logic, request)
            future_view2 = executor.submit(festival_now_view_logic)

            data['nowview_response'] = future_view2.result()
            data['listview_response'] = future_view1.result()
            month_dict = {}
            for i in range(1, 13):
                month_dict[str(i)] = str(i).zfill(2)
            area_dict = {}
            for i in AreaCode.objects.all():
                if i.name not in area_dict:
                    area_dict[i.name] = i.code
            data['month_dict'] = month_dict
            data['area_dict'] = area_dict

        return JsonResponse(data)

########################################### 복붙 ###########################################
# @login_required(login_url='/member/login')
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['GET', 'POST'])
def like(request,content_id):
    # 어떤 게시물에, 어떤 사람이 like를 했는 지
    if request.method == 'POST':
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