from django.db import models

# Create your models here.
from django.db import models
from system.storage import ImageStorage

# Create your models here.

class mypicture(models.Model):
    phone = models.CharField(max_length=64)
    photo = models.ImageField(upload_to='photos', default='', storage=ImageStorage())

class invationRecord(models.Model):
    date = models.DateField()
    time = models.TimeField()
    level = models.IntegerField()
    camera_id = models.IntegerField()
    area = models.CharField(max_length= 50)
    invation_num =models.IntegerField()

class WhiteList(models.Model):
    name = models.CharField(max_length=20)
    level = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    time_start =models.TimeField()
    time_end = models.TimeField()

class segmentation(models.Model):
    left = models.CharField(max_length=20)
    top = models.CharField(max_length=20)
    width = models.CharField(max_length=20)
    height = models.CharField(max_length=20)
    level = models.CharField(max_length=20)

class mytask(models.Model):
    uid = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    status = models.IntegerField()
    origin = models.ImageField(upload_to='tasks', default='', storage=ImageStorage())
    processed = models.ImageField(upload_to='processed', default='', storage=ImageStorage())

class FallEvent(models.Model):
    cid = models.IntegerField() # camera id
    date = models.DateField()
    time = models.TimeField()
    detail = models.CharField(max_length= 200)

class InteractionEvent(models.Model):
    cid = models.IntegerField() # camera id
    vid = models.IntegerField() # volunteer id
    oid = models.IntegerField() # older id
    date = models.DateField()
    time = models.TimeField()
    detail = models.CharField(max_length= 200)

class EmoEvent(models.Model):
    cid = models.IntegerField() # camera id
    oid = models.IntegerField() # older id
    date = models.DateField()
    time = models.TimeField()
    detail = models.CharField(max_length= 200)


