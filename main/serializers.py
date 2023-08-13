from rest_framework import serializers

from main.models import Review, Tour



class ReviewWithTourSerializer(serializers.ModelSerializer):
    tour = serializers.CharField(source="content_id.title", read_only=True)
    real_content_id = serializers.CharField(source='content_id.content_id', read_only=True)

    class Meta:
        model = Review
        fields = ['content_id', 'title', 'content', 'rank', 'created_at', 'updated_at', 'tour', 'real_content_id']
        read_only_fields = ['content_id', 'created_at', 'updated_at']

class MainBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ['content_id', 'title', 'first_image']
