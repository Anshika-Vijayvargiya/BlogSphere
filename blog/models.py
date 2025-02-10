from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    i=[("Draft","draft"),("Published","Published")]
    
    title=models.CharField(max_length=100)
    #author=models.CharField(max_length=30)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.TextField()
    status=models.CharField(max_length=30,choices=i,default="draft")
    curr=models.DateTimeField(auto_now_add=True)
    up_date=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.title
    

class Favourite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)

    def __str__(self):
        return self.blog.title