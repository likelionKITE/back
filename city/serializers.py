from rest_framework import serializers
from main.models import Tour

# Create your serializers here.
class CitySerializer(serializers.ModelSerializer):
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