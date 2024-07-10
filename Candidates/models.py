from django.db import models
import datetime
import os

# Create your models here.

def filePath(request,filename):
    oldname = filename
    timenow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = '%s%s'%(timenow,oldname)
    return os.path.join('static/uploads/',filename)

class admins(models.Model):
    adminuserid = models.CharField(max_length = 100,blank = False,null = False)
    password = models.CharField(max_length = 100,blank = False, null = False) 

class Electioncandidates(models.Model):
    candidateID = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100,unique=True)
    age = models.PositiveIntegerField()
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,blank=False)
    education = models.CharField(max_length=255,blank=False)
    photo = models.ImageField(upload_to=filePath, blank=False)
    party_name = models.CharField(max_length=100,blank=False,unique=True)
    party_symbol = models.ImageField(upload_to=filePath, blank=False)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    votes = models.PositiveIntegerField(default=0)
