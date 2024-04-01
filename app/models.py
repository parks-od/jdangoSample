from django.db import models
from django.utils import timezone


# Create your models here.
#### 메뉴 : 상위종류, 이름, 종가 or 가격, 코드, 생성 or 추가일
class Asset(models.Model):
    parentCode = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    code = models.CharField(max_length=20, primary_key=True)
    today_range = models.DecimalField(max_digits=10, decimal_places=2)
    create_date = models.DateTimeField(default=timezone.now(), blank=True)
