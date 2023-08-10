from rest_framework import serializers
from main.models import Tour, AreaCode, ServiceCode, DetailCommon

# Create your serializers here.

class CitySerializer(serializers.ModelSerializer):
    area_code = serializers.CharField(source="sigungu_code.name", read_only=True)
    sigungu_code = serializers.CharField(source="sigungu_code.sigungu_name", read_only=True)
    cat1 = serializers.CharField(source="cat3.main_name", read_only=True)
    cat2 = serializers.CharField(source="cat3.mid_name", read_only=True)
    cat3 = serializers.CharField(source="cat3.sub_name", read_only=True)

    class Meta:
        model = Tour
        fields = ["id", 
                "addr1",
                "addr2",
                "area_code",
                "cat1",
                "cat2",
                "cat3", 
                "content_id",
                "content_type_id",
                "first_image",
                "first_image2",
                "cpyrhtDivCd",
                "mapx",
                "mapy",
                "mlevel",
                "modified_time",
                "sigungu_code",
                "tel",
                "title"]