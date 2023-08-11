from django.shortcuts import render
from main.models import ServiceCode, AreaCode, Tour, DetailInfo, DetailCommon
from .models import DetailIntroTravel
from rest_framework import generics
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from .serializers import TravelSerializer

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
                fields = ('title', 'first_image2', 'sido_part', 'sigungu_part', 'content_id')

class TravelPagination(LimitOffsetPagination):
    default_limit = 20

#===================================================================================================

class TravelListView(generics.ListAPIView):
    # queryset = Tour.objects.filter(content_type_id="76")
    serializer_class = CustomTravelSerializer
    pagination_class = TravelPagination

    def get_queryset(self):
        cat1_selected = self.request.GET.get('cat1')
        cat2_selected = self.request.GET.get('cat2')
        
        queryset = Tour.objects.filter(content_type_id="76")  # 여행지 데이터 가져오기
        
        if cat1_selected:
            queryset = queryset.filter(cat1=cat1_selected)
        
        if cat2_selected:
            queryset = queryset.filter(cat2=cat2_selected)
        
        return queryset

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
        serialized_instance = self.serializer_class(instance=instance).data
        result = [serialized_instance]  # 결과를 리스트에 추가
        return Response(result)

    # def get_serializer_class(self):
    #     return CustomTravelSerializer

# class TravelFindView(generics.ListAPIView):
#     serializer_class = CustomTravelSerializer  # 사용할 Serializer 클래스 설정
#     pagination_class = TravelPagination  # 페이지네이션 클래스 설정
    
#     def get_queryset(self):
#         cat1_selected = self.request.GET.get('cat1')
#         cat2_selected = self.request.GET.get('cat2')
        
#         queryset = Tour.objects.filter(content_type_id="76")  # 여행지 데이터 가져오기
        
#         if cat1_selected:
#             queryset = queryset.filter(cat1=cat1_selected)
        
#         if cat2_selected:
#             queryset = queryset.filter(cat2=cat2_selected)
        
#         return queryset