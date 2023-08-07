from django.db import models


# Create your models here.

from main.models import Tour


class DetailIntroTravel(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    content_id = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='detail_intro_travel')
    heritage1 = models.CharField(max_length=1)
    accom_count = models.CharField(max_length=10)
    exp_age_range = models.CharField(max_length=10)
    exp_guide = models.TextField(default='')
    info_center = models.CharField(max_length=30)
    open_date = models.CharField(max_length=30)
    parking =models.CharField(max_length=10)
    rest_date = models.CharField(max_length=30)
    use_season = models.CharField(max_length=30)
    use_time = models.CharField(max_length=30)