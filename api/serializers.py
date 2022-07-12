from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from api.models import Blogs,Comment
from django.contrib.auth.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=["id","first_name","last_name","username","email","password"]

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class BlogsSerializer(ModelSerializer):
    author =serializers.CharField(read_only=True)
    user   = serializers.CharField(read_only=True)

    class Meta:
        model=Blogs
        exclude=("posted_date",)
        depth=1

    def create(self, validated_data):
        user=self.context.get("user")
        return Blogs.objects.create(**validated_data,author=user)


class CommentSerializer(ModelSerializer):
    user=serializers.CharField(read_only=True)
    blogs = serializers.CharField(read_only=True)
    class Meta:
        model=Comment
        fields=["blogs",'comment',"user"]

    def create(self, validated_data):
        user=self.context.get("user")
        blog=self.context.get("blog")
        return Comment.objects.create(**validated_data,blog=blog,user=user)




