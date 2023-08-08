from django.shortcuts import render
from main.models import ServiceCode, AreaCode, Tour, DetailInfo
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import serializers
from .serializers import CitySerializer
import requests

# Create your views here.

class CityListView(generics.ListAPIView):
    queryset = Tour.objects.all()

    def get_serializer_class(self):
        # 'addr1'에서 "(특별)시/도"와 "시/군/구" 부분을 추출하는 커스텀 Serializer 클래스 생성
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
                fields = ('title', 'first_image', 'sido_part', 'sigungu_part')

        return CustomCitySerializer

