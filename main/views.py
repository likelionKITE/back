from django.shortcuts import render

# Create your views here.
from main.models import Tour, Review
from django.db.models import Count

from main.serializers import MainBannerSerializer, ReviewWithTourSerializer
from festival.serializers import FestivalSerializer
from concurrent.futures import ThreadPoolExecutor
from django.http import JsonResponse
from convert_to_queryset import list_to_queryset


def banner_list_view_logic():
    queryset = Tour.objects.filter(content_type_id="76").order_by('?')[:4]
    serializer = MainBannerSerializer(queryset, many=True)
    return serializer.data

def most_liked_travel_list_view_logic():
    queryset = Tour.objects.filter(content_type_id="76").annotate(count=Count('like_users')).order_by('-count')[:13]
    serializer = FestivalSerializer(queryset, many=True)
    return serializer.data

def theme_festival_view_logic(request):
    queryset = Tour.objects.filter(content_type_id="85")
    serializer = FestivalSerializer(queryset, many=True)
    flower = queryset.filter(detailCommon__overview__icontains='flower')
    food = queryset.filter(detailCommon__overview__icontains='food')
    traditional = queryset.filter(detailCommon__overview__icontains='traditional')
    serialized_data = {}

    # 각각의 필터링된 데이터를 직렬화하여 저장
    serialized_data['flower'] = FestivalSerializer(flower, many=True).data
    serialized_data['food'] = FestivalSerializer(food, many=True).data
    serialized_data['traditional'] = FestivalSerializer(traditional, many=True).data

    return serialized_data

def good_review_list_view_logic():
    queryset = Review.objects.filter(rank=5)
    serializer = ReviewWithTourSerializer(queryset, many=True)
    return serializer.data


def MainCombinedView(request):
    data = {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_view1 = executor.submit(banner_list_view_logic)
        future_view2 = executor.submit(most_liked_travel_list_view_logic)
        future_view3 = executor.submit(theme_festival_view_logic, request)
        future_view4 = executor.submit(good_review_list_view_logic)

        data['bannerlist_response'] = future_view1.result()
        data['mostlikedtravel_response'] = future_view2.result()
        data['themefestival_response'] = future_view3.result()
        data['goodreview_response'] = future_view4.result()

    return JsonResponse(data)
