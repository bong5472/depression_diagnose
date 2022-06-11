from django.db import models
from user.models import Device

# Create your models here.

class Log(models.Model):
    l_Id = models.AutoField(primary_key=True)
    logDate = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null= False)
    deviceId = models.ForeignKey(Device, on_delete=models.CASCADE, db_column='deviceId')

    def __str__(self):
        return self.title