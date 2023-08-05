from django.db import models

# Create your models here.
from main.models import ServiceCode


class DetailIntroFest(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    content_id = models.ForeignKey(ServiceCode, on_delete=models.CASCADE, related_name='detail_intro_fest')
    place_info = models.TextField(default='')
    event_homepage = models.URLField(max_length=1024)
    event_place = models.CharField(max_length=40)
    play_time = models.CharField(max_length=30)
    program = models.TextField(default='')
    age_limit = models.CharField(max_length=30)
    spend_time_festival =models.CharField(max_length=30)
    booking_place = models.CharField(max_length=30)
    discount_info_festival = models.CharField(max_length=30)
    event_start_date = models.CharField(max_length=30)
    event_end_date = models.CharField(max_length=30)
    sponsor1 = models.CharField(max_length=30)
    sponsor1tel = models.CharField(max_length=30)
    sponsor2 = models.CharField(max_length=30)
    sponsor2tel = models.CharField(max_length=30)
    sub_event = models.CharField(max_length=30)
    use_time_festival = models.CharField(max_length=30)