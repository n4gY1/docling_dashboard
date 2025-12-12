

from django.db import models


# Create your models here.
class GeneratedRag(models.Model):
    filename = models.CharField(max_length=150,unique=True)
    path = models.CharField(max_length=200,null=True)
    created_at = models.DateTimeField(auto_created=True,auto_now_add=True)
    errors = models.CharField(max_length=500,blank=True)
    finished_at = models.DateTimeField(null=True,blank=True)

    lines = models.IntegerField(default=0)
    content = models.CharField(max_length=150,blank=True)

