from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to="pro-pic",null=True)
    bio=models.CharField(max_length=120,null=True)

class Blogs(models.Model):
    title_name = models.CharField(max_length=20)
    discription=models.CharField(max_length=200)
    image=models.ImageField(upload_to="blogs_pic",null=True)
    posted_date=models.DateTimeField(auto_now_add=True,null=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="authers")
    liked_by=models.ManyToManyField(User)


    def __str__(self):
        return self.title_name

class Comment(models.Model):
    blog=models.ForeignKey(Blogs,on_delete=models.CASCADE)
    comment=models.CharField(max_length=120)
    user=models.ForeignKey(User,on_delete=models.CASCADE)





