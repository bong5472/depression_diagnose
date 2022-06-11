from django.db import models

# Create your models here.

class User(models.Model):
    userId = models.AutoField(primary_key=True)
    Id = models.CharField(max_length=25, null=False, unique=True)
    Pw = models.CharField(max_length=256, null=False)
    userName = models.CharField(max_length=15, null=False)


class Device(models.Model):
    deviceId = models.CharField(max_length=10, primary_key=True)
    userId = models.ForeignKey('User', on_delete=models.CASCADE, db_column='userId')


class deviceToken(models.Model):
    t_Id = models.AutoField(primary_key=True)
    deviceId = models.ForeignKey('Device', on_delete=models.CASCADE, db_column="deviceId")
    token = models.CharField(max_length=2000, null=False)
