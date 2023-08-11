from rest_framework import serializers

from main.models import Tour

from festival.models import DetailIntroFest


class FestivalSerializer_all(serializers.ModelSerializer):

        class Meta:
                model = Tour
                fields = [
                        "content_id",
                        "first_image2",
                        "title",
                ]

        # def get_event_start_date(self, obj):
        #         try:
        #                 detail_intro_fest = DetailIntroFest.objects.get(content_id=obj.id)
        #                 return detail_intro_fest.event_start_date
        #         except DetailIntroFest.DoesNotExist:
        #                 return None
        #
        # def get_event_end_date(self, obj):
        #         try:
        #                 detail_intro_fest = DetailIntroFest.objects.get(content_id=obj.id)
        #                 return detail_intro_fest.event_end_date
        #         except DetailIntroFest.DoesNotExist:
        #                 return None

class FestivalSerializer_now(serializers.ModelSerializer):
        event_start_date = serializers.SerializerMethodField()
        event_end_date = serializers.SerializerMethodField()

        class Meta:
                model = Tour
                fields = [
                        "content_id",
                        "first_image2",
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