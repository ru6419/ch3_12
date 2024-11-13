from django.db import models

class students(models.Model): # 類別_資料庫名稱
    cID = models.AutoField(primary_key=True)
    cName = models.CharField(max_length=20, blank=False)
    cSex = models.CharField(max_length=1, blank=False, default='F')
    cBirthday = models.DateField(blank=False)
    cEmail = models.CharField(max_length=100, blank=False)
    cPhone = models.CharField(max_length=20, blank=False)
    cAddr = models.CharField(max_length=255, blank=False)
    cHeight = models.IntegerField(blank=True, null=True)
    cWeight = models.IntegerField(blank=True, null=True)
