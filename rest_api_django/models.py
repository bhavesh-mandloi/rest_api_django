from django.db import models

class IoT_Data(models.Model):
    Serial_no =  models.IntegerField()
    Device_id = models.CharField(max_length=50)
    Device_name = models.CharField(max_length=500)
    tempt_sensor = models.CharField(max_length=10)
    press_sensor = models.CharField(max_length=10)

    def __str__ (self):
        return self.Device_name+' '+self.Device_id 
    
