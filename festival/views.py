from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from django.db import models
from django.http import JsonResponse

from django.shortcuts import render
from rest_framework import generics

# Create your views here.
from main.models import Tour, AreaCode

from django.db.models import Q

from festival.serializers import FestivalSerializer, FestivalSerializer_now, FestivalDetailSerializer


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


class FestivalSearchView(generics.ListAPIView):

    serializer_class = FestivalSerializer
    def get_queryset(self):
        nowyear = datetime.today().strftime("%Y")
        month_selected = self.request.GET.get('month')
        area_selected = self.request.GET.get('area_code')

        queryset = Tour.objects.filter(content_type_id="85").annotate(
        event_start_date=models.F('detail_intro_fest__event_start_date'),
        event_end_date=models.F('detail_intro_fest__event_end_date')
    )  # 여행지 데이터 가져오기

        if month_selected:
            queryset = queryset.filter(Q(event_start_date__contains=nowyear+month_selected)|Q(event_end_date__contains=nowyear+month_selected))

        if area_selected:
            queryset = queryset.filter(area_code=area_selected)

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
