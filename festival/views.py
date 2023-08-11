from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from django.db import models
from django.http import JsonResponse

from django.shortcuts import render
from rest_framework import generics

# Create your views here.
from main.models import Tour, AreaCode

from festival.serializers import FestivalSerializer_all, FestivalSerializer_now


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
    serializer = FestivalSerializer_all(queryset, many=True)
    return serializer.data

def festival_now_view_logic():
    nowdate = datetime.today().strftime("%Y%m%d")
    queryset = Tour.objects.filter(content_type_id="85").annotate(
        event_start_date=models.F('detail_intro_fest__event_start_date'),
        event_end_date=models.F('detail_intro_fest__event_end_date')
    ).filter(event_start_date__lte=nowdate, event_end_date__gte=nowdate).order_by('?')[:4]
    serializer = FestivalSerializer_now(queryset, many=True)
    return serializer.data



# 여러 뷰의 결과를 한 url에서 동시에 내보내기 - 근데 이렇게 하려면 view를 클래스형태가 아니라 저렇게 함수 형태로 구현해야 한대
def FestivalCombinedView_main(request):
    data = {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_view1 = executor.submit(festival_list_view_logic)
        future_view2 = executor.submit(festival_now_view_logic)

        data['listview_response'] = future_view1.result()
        data['nowview_response'] = future_view2.result()

    return JsonResponse(data)


