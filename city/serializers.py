from rest_framework import serializers
from main.models import Tour, AreaCode, ServiceCode, DetailCommon, Review
from travel.models import DetailIntroTravel
from festival.models import DetailIntroFest

# Create your serializers here.
class CityReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source = 'user.nickname')
    class Meta:
        model = Review
        fields = ['content_id', 'user', 'title', 'content', 'rank', 'created_at', 'updated_at']
        extra_kwargs = {'content_id': {'write_only': True}}

class DetailIntroTrvSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailIntroTravel
        exclude = ['id', 'content_id']

class DetailIntroFestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailIntroFest
        exclude = ['id', 'content_id']

class DetailCommonSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailCommon
        fields = ['title', 'modified_time', 'overview', 'homepage']

class CitySerializer(serializers.ModelSerializer):
    # area_code = serializers.CharField(source="sigungu_code.name", read_only=True)
    sigungu_code = serializers.CharField(source="sigungu_code.sigungu_name", read_only=True)
    cat1 = serializers.CharField(source="cat3.main_name", read_only=True)
    cat2 = serializers.CharField(source="cat3.mid_name", read_only=True)
    cat3 = serializers.CharField(source="cat3.sub_name", read_only=True)
    
    detailCommon = DetailCommonSerializer(many=True, read_only=True)
    detail_intro_travel = DetailIntroTrvSerializer(many=True, read_only=True)
    detail_intro_fest = DetailIntroFestSerializer(many=True, read_only=True)
    reviews = CityReviewSerializer(many=True, read_only=True)

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
                "detail_intro_fest",
                "reviews"]