from django.db import models

# Create your models here.

class ServiceCode(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    maincode = models.CharField(max_length=40)
    mainname = models.CharField(max_length=40)
    midcode = models.CharField(max_length=40)
    midname = models.CharField(max_length=40)
    subcode = models.CharField(max_length=40)
    subname = models.CharField(max_length=40)

    # def __str__(self):
    #     return self.name

class AreaCode(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    code = models.CharField(max_length=40)
    sigungucode = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    sigunguname = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Tour(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    addr1 = models.TextField(default='')
    addr2 = models.TextField(default='')
    areacode = models.ForeignKey(AreaCode, on_delete=models.CASCADE, related_name='AreaCode')
    cat1 = models.ForeignKey(ServiceCode, on_delete=models.CASCADE, related_name='cat1')
    cat2 = models.ForeignKey(ServiceCode, on_delete=models.CASCADE, related_name='cat2')
    cat3 = models.ForeignKey(ServiceCode, on_delete=models.CASCADE, related_name='cat3')
    contentid = models.ForeignKey(ServiceCode, on_delete=models.CASCADE, related_name='ContentId')
    contenttypeid = models.ForeignKey(ServiceCode, on_delete=models.CASCADE, related_name='ContentTypeid')
    firstimage = models.URLField(max_length=1024)
    firstimage2 = models.URLField(max_length=1024)
    cpyrhtDivCd = models.CharField(max_length=40)
    mapx = models.CharField(max_length=50)
    mapy = models.CharField(max_length=50)
    mlevel = models.CharField(max_length=20)
    modifiedtime = models.CharField(max_length=50)
    sigungucode = models.ForeignKey(AreaCode, on_delete=models.CASCADE, related_name='SigunguCode')
    tel = models.TextField(default='')
    title = models.TextField(default='')

    def __str__(self):
        return self.title

