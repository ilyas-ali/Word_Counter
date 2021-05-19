from django.db import models

# Create your models here.
class Counter(models.Model):
    urllink=models.URLField(max_length = 200)
    words = models.TextField(null=True)