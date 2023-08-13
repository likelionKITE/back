from rest_framework import serializers
from main.models import Tour, AreaCode, ServiceCode, DetailInfo, DetailCommon, Review
from .models import DetailIntroTravel

# Create your serializers here.
class TravelReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.nickname')
    class Meta:
        model = Review
        fields = ['content_id', 'user', 'title', 'content', 'rank', 'created_at', 'updated_at']
        extra_kwargs = {'content_id': {'write_only': True}}

class DetailCommonSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailCommon
        fields = ['title', 'modified_time', 'overview', 'homepage']

class DetailIntroTrvSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailIntroTravel
        fields = '__all__'

class TravelSerializer(serializers.ModelSerializer):
    area_code = serializers.CharField(source="sigungu_code.name", read_only=True)
    sigungu_code = serializers.CharField(source="sigungu_code.sigungu_name", read_only=True)
    cat3 = serializers.CharField(source="cat3.sub_name", read_only=True)

    detailCommon = DetailCommonSerializer(many=True, read_only=True)
    detail_intro_travel = DetailIntroTrvSerializer(many=True, read_only=True)
    reviews = TravelReviewSerializer(many=True, read_only=True)

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
                "title",
                "detailCommon",
                "detail_intro_travel",
                "reviews"]