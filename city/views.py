from django.shortcuts import render
from main.models import ServiceCode, AreaCode, Tour, DetailInfo, DetailCommon
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import serializers
from .serializers import CitySerializer
import requests
from datetime import datetime
from django.db.models import Q

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
                fields = ('title', 'first_image2', 'sido_part', 'sigungu_part', 'content_id', 'content_type_id')

class CityPagination(LimitOffsetPagination):
    default_limit = 20
#===================================================================================================

class CityTravelListView(generics.ListAPIView):
    serializer_class = CustomCitySerializer
    pagination_class = CityPagination

    def get_queryset(self):
        area_selected = self.request.GET.get('area_code')
        queryset = Tour.objects.filter(content_type_id="76")  # 해당 지역의 여행지 데이터 가져오기
        if area_selected:
            queryset = queryset.filter(area_code=area_selected)
        return queryset

class CityFestListView(generics.ListAPIView):
    serializer_class = CustomCitySerializer
    pagination_class = CityPagination

    def get_queryset(self):
        area_selected = self.request.GET.get('area_code')
        current_month = datetime.today().strftime("%Y%m")

        queryset = Tour.objects.filter(content_type_id="85")  # 해당 지역의 축제 데이터 가져오기
        if area_selected:
            queryset = queryset.filter(area_code=area_selected)
        
        queryset = queryset.filter(
            Q(detail_intro_fest__event_start_date__contains=current_month) |
            Q(detail_intro_fest__event_end_date__contains=current_month)
        )

        return queryset

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

class CityTotalListView(generics.ListAPIView):
    serializer_class = CustomCitySerializer
    pagination_class = CityPagination

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
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)





