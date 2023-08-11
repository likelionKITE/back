from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from django.db import models
from django.http import JsonResponse

from django.shortcuts import render
from rest_framework import generics

# Create your views here.
from main.models import Tour, AreaCode

from festival.serializers import FestivalSerializer, FestivalSerializer_now, FestivalDetailSerializer


# class FestivalListView(generics.ListAPIView):
#     serializer_class = FestivalSerializer_all
#     queryset = Tour.objects.filter(content_type_id="85")
#
#
# class FestivalNowView(generics.ListAPIView):
#     serializer_class = FestivalSerializer_now
#     nowdate = datetime.today().strftime("%Y%m%d")
#     queryset = Tour.objects.filter(content_type_id="85").annotate(event_start_date=models.F('detail_intro_fest__event_start_date'),
#         event_end_date=models.F('detail_intro_fest__event_end_date')).order_by('?')[:4]


def festival_list_view_logic():
    queryset = Tour.objects.filter(content_type_id="85")
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


def festival_search_view_logic():
    def get_queryset(self):
        cat1_selected = self.request.GET.get('cat1')
        cat2_selected = self.request.GET.get('cat2')

        queryset = Tour.objects.filter(content_type_id="85")  # 여행지 데이터 가져오기

        if cat1_selected:
            queryset = queryset.filter(cat1=cat1_selected)

        if cat2_selected:
            queryset = queryset.filter(cat2=cat2_selected)

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

# 여러 뷰의 결과를 한 url에서 동시에 내보내기 - 근데 이렇게 하려면 view를 클래스형태가 아니라 저렇게 함수 형태로 구현해야 한대
def FestivalCombinedView_main(request):
    data = {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_view1 = executor.submit(festival_list_view_logic)
        future_view2 = executor.submit(festival_now_view_logic)

        data['nowview_response'] = future_view2.result()
        data['listview_response'] = future_view1.result()


    return JsonResponse(data)


