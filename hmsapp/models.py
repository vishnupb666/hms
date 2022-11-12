from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here


class role(models.Model):
    name = models.CharField(max_length=255)
    
class department(models.Model):
    name = models.CharField(max_length=255)

class user_ext(models.Model):
    user_id = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    phone = models.IntegerField()
    image = models.ImageField(upload_to='user/pro_pic')
    gender = models.CharField(max_length=255)
    dob = models.DateField(default=datetime.date.today,null=True)
    address = models.CharField(max_length=255)
    rol_id =models.ForeignKey(role,on_delete=models.CASCADE,null=True,blank=True) 

class doctor(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True) 
    dep_id = models.ForeignKey(department,on_delete=models.CASCADE,null=True,blank=True)
    

class appointment(models.Model):
    user_id = models.ForeignKey(user_ext,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(null=True)
    doc_id = models.ForeignKey(doctor,on_delete=models.CASCADE,null=True,blank=True)
    requested = models.IntegerField(null=True)
    Approved = models.IntegerField(null=True)
    department = models.ForeignKey(department,on_delete=models.CASCADE,null=True,blank=True)
    time = models.TimeField(null=True)
class leave(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    doc_id = models.ManyToManyField(doctor,blank=True,)
    leave_date = models.DateField(null=True)
    reason = models.CharField(max_length=250)
    approve = models.IntegerField(null=True)
