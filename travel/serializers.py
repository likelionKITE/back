from rest_framework import serializers
from main.models import Tour, AreaCode, ServiceCode, DetailInfo, DetailCommon
from .models import DetailIntroTravel

# Create your serializers here.

class TravelSerializer(serializers.ModelSerializer):
    area_code = serializers.CharField(source="sigungu_code.name", read_only=True)
    sigungu_code = serializers.CharField(source="sigungu_code.sigungu_name", read_only=True)
    cat3 = serializers.CharField(source="cat3.sub_name", read_only=True)

    class Meta:
        model = Tour
        fields = '__all__'