from django.db import models


class Surprise(models.Model):
    link = models.URLField(max_length=500)
    description = models.TextField(max_length=1000)
