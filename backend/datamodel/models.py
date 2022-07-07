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
    img = models.ImageField(upload_to='falls', default='', storage=ImageStorage())

class InteractionEvent(models.Model):
    cid = models.IntegerField() # camera id
    vid = models.IntegerField() # volunteer id
    oid = models.IntegerField() # older id
    date = models.DateField()
    time = models.TimeField()
    detail = models.CharField(max_length= 200)
    img = models.ImageField(upload_to='actions', default='', storage=ImageStorage())

class EmoEvent(models.Model):
    cid = models.IntegerField() # camera id
    oid = models.IntegerField() # older id
    date = models.DateField()
    time = models.TimeField()
    detail = models.CharField(max_length= 200)
    emo = models.CharField(max_length=10,default='')
    img = models.ImageField(upload_to='emos', default='', storage=ImageStorage())

class UnkownEvent(models.Model):
    cid = models.IntegerField() # camera id
    date = models.DateField()
    time = models.TimeField()
    num = models.IntegerField()
    detail = models.CharField(max_length= 200)
    img = models.ImageField(upload_to='unkowns', default='', storage=ImageStorage())

class AttackEvent(models.Model):
    cid = models.IntegerField() # camera id
    personType = models.CharField(max_length= 20)
    area = models.CharField(max_length= 20)
    personId = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    detail = models.CharField(max_length= 200)
    img = models.ImageField(upload_to='attacks', default='', storage=ImageStorage())

class Older(models.Model):
    name = models.CharField(max_length= 20)
    gender = models.CharField(max_length= 4)
    age = models.IntegerField()
    idcard = models.CharField(max_length= 30)
    phone = models.CharField(max_length= 30)
    room = models.CharField(max_length= 10)

    r1name = models.CharField(max_length= 20)
    r1phone = models.CharField(max_length= 30)
    r2name = models.CharField(max_length= 20)
    r2phone = models.CharField(max_length= 30)
    health = models.CharField(max_length= 200)
    regdate = models.DateField()

class Stuff(models.Model):
    name = models.CharField(max_length= 20)
    gender = models.CharField(max_length= 4)
    age = models.IntegerField()
    idcard = models.CharField(max_length= 30)
    phone = models.CharField(max_length= 30)

    regdate = models.DateField()

class Volunteer(models.Model):
    name = models.CharField(max_length= 20)
    gender = models.CharField(max_length= 4)
    age = models.IntegerField()
    idcard = models.CharField(max_length= 30)
    phone = models.CharField(max_length= 30)

    regdate = models.DateField()

class FaceLib(models.Model):
    idcard = models.CharField(max_length=64)
    img = models.ImageField(upload_to='faces', default='', storage=ImageStorage())
