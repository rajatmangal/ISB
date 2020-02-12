
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    text = models.CharField(max_length=400, null=True)
    description = models.TextField(max_length=2000, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    userid = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.text + str(self.id)


class PostComment(models.Model):
    text = models.CharField(max_length=2000, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    userid = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    postid = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.text + str(self.id)