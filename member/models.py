from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class CustomUser(AbstractUser):
    REQUIRED_FIELDS = []
    email = None
    nickname = models.CharField(max_length=100)

    #여기서 related_name 설정을 안해주면 계속 역참조 에러가 남.
    groups = models.ManyToManyField(Group, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users_permissions')