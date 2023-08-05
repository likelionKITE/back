from django.db import models

# Create your models here.

class ServiceCode(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    main_code = models.CharField(max_length=40)
    main_name = models.CharField(max_length=40)
    mid_code = models.CharField(max_length=40)
    mid_name = models.CharField(max_length=40)
    sub_code = models.CharField(max_length=40)
    sub_name = models.CharField(max_length=40)

    # def __str__(self):
    #     return self.name

class AreaCode(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    code = models.CharField(max_length=40)
    sigungu_code = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    sigungu_name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Tour(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    addr1 = models.TextField(default='')
    addr2 = models.TextField(default='')
    area_code = models.ForeignKey(AreaCode, on_delete=models.CASCADE, related_name='tour_area')
    cat1 = models.ForeignKey(ServiceCode, on_delete=models.CASCADE, related_name='tour_cat1')
    cat2 = models.ForeignKey(ServiceCode, on_delete=models.CASCADE, related_name='tour_cat2')
    cat3 = models.ForeignKey(ServiceCode, on_delete=models.CASCADE, related_name='tour_cat3')
    content_id = models.CharField(max_length=40)
    content_type_id = models.ForeignKey(ServiceCode, on_delete=models.CASCADE, related_name='tour_type')
    first_image = models.URLField(max_length=1024)
    first_image2 = models.URLField(max_length=1024)
    cpyrhtDivCd = models.CharField(max_length=40)
    mapx = models.CharField(max_length=50)
    mapy = models.CharField(max_length=50)
    mlevel = models.CharField(max_length=20)
    modified_time = models.CharField(max_length=50)
    sigungu_code = models.ForeignKey(AreaCode, on_delete=models.CASCADE, related_name='tour_sigungu')
    tel = models.TextField(default='')
    title = models.TextField(default='')

    def __str__(self):
        return self.title

class DetailInfo(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    info_name = models.CharField(max_length=40)
    content_id = models.CharField(max_length=40)
    content_type_id = models.ForeignKey(AreaCode, on_delete=models.CASCADE, related_name='detailinfo_type')
    fidgubun = models.CharField(max_length=40)
    info_text = models.TextField(default='')
    serial_num = models.CharField(max_length=40)

class DetailCommon(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    overview = models.TextField(default='')
    tel_Name = models.CharField(max_length=50)
    title = models.CharField(max_length=90)
    modified_time = models.CharField(max_length=50)
    homepage = models.TextField(default='')
    content_id = models.ForeignKey(ServiceCode, on_delete=models.CASCADE, related_name='detailcommon_contentid')
    cpyrhtDivCd = models.TextField(default='')