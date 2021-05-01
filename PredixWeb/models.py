from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

# Create your models here.
class Movies(models.Model):
    mid = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    rating = models.CharField(max_length=5, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, blank=True)
    genre = models.CharField(max_length=255, null=True, blank=True)
    rdate = models.CharField(max_length=255, null=True, blank=True)
    language = models.CharField(max_length=255, null=True, blank=True)
    cover = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    sequal = models.CharField(max_length=255, null=True, blank=True)
    trailer = models.CharField(max_length=255, null=True, blank=True)
    year = models.CharField(max_length=5, null=True, blank=True)
    objects = models.Manager()
    
    def __str__(self) -> str:
        return self.title   
    
class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    uid = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        return "Query from " + str(self.name)
    
class Cast(models.Model):
    mid = models.ForeignKey(Movies, on_delete=CASCADE)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length = 255)
    role = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    objects = models.Manager()

class MyMovies(models.Model):
    mid = models.ForeignKey(Movies, on_delete=CASCADE)
    uid = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    watched = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()   
    
class Notifications(models.Model):
    nid = models.AutoField(primary_key=True)
    mid = models.ForeignKey(Movies, on_delete=CASCADE)
    message = models.CharField(max_length=255)
    ndate = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()