from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    topic = models.ForeignKey(Topic, null=True, on_delete=SET_NULL) # each Post is related to a single Topic
    user = models.ForeignKey(User, null=True, on_delete=SET_NULL) # each Post is related to a single User
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
        