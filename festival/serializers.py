from rest_framework import serializers

from main.models import Tour, DetailCommon

from main.serializers import MainReviewSerializer

from festival.models import DetailIntroFest

from city.serializers import DetailCommonSerializer

# Create your serializers here.
class DetailIntroFestSerializer(serializers.ModelSerializer):

        class Meta:
                model = DetailIntroFest
                fields = [
                        "place_info",
                        "event_homepage",
                        "event_place",
                        "play_time",
                        "program",
                        "age_limit",
                        "spend_time_festival",
                        "booking_place",
                        "discount_info_festival",
                        "event_start_date",
                        "event_end_date",
                        "sub_event",
                        "use_time_festival"
                ]

class FestivalSerializer(serializers.ModelSerializer):

        class Meta:
                model = Tour
                fields = [
                        "content_id",
                        "first_image",
                        "title",
                ]


class FestivalSerializer_now(serializers.ModelSerializer):
        event_start_date = serializers.SerializerMethodField()
        event_end_date = serializers.SerializerMethodField()

        class Meta:
                model = Tour
                fields = [
                        "content_id",
                        "first_image",
                        "title",
                        "event_start_date",
                        "event_end_date",
                ]

        def get_event_start_date(self, obj):
                try:
                        detail_intro_fest = DetailIntroFest.objects.get(content_id=obj.id)
                        return detail_intro_fest.event_start_date
                except DetailIntroFest.DoesNotExist:
                        return None

        def get_event_end_date(self, obj):
                try:
                        detail_intro_fest = DetailIntroFest.objects.get(content_id=obj.id)
                        return detail_intro_fest.event_end_date
                except DetailIntroFest.DoesNotExist:
                        return None

class FestivalDetailSerializer(serializers.ModelSerializer):
        area_code = serializers.CharField(source="sigungu_code.name", read_only=True)
        sigungu_code = serializers.CharField(source="sigungu_code.sigungu_name", read_only=True)
        cat1 = serializers.CharField(source="cat3.main_name", read_only=True)
        cat2 = serializers.CharField(source="cat3.mid_name", read_only=True)
        cat3 = serializers.CharField(source="cat3.sub_name", read_only=True)
        like_users = serializers.CharField(source="like_users.id", read_only=True)
        detailCommon = DetailCommonSerializer(many=True, read_only=True)
        detail_intro_fest = DetailIntroFestSerializer(many=True, read_only=True)
        reviews = MainReviewSerializer(many=True, read_only=True)

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
                          # "first_image2",
                          "cpyrhtDivCd",
                          "mapx",
                          "mapy",
                          "mlevel",
                          "modified_time",
                          "sigungu_code",
                          "tel",
                          "title",
                          "detailCommon",
                          "detail_intro_fest",
                          "reviews",
                          "like_users"]
