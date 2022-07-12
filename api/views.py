from django.shortcuts import render
from rest_framework.views import APIView
from api.models import Blogs,Comment
from rest_framework.response import Response
from api.serializers import BlogsSerializer,CommentSerializer,UserSerializer
from rest_framework import permissions,authentication
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin
from  rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

# Create your views here.

class BlogsView(APIView):
    authentication_classes = [authentication.BasicAuthentication,authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get(self,request,*args,**kwargs):
        qs=Blogs.objects.all()
        serializer=BlogsSerializer(qs,many=True)
        return Response(serializer.data)

    def post(self,request,*args,**kwargs):
        serializer=BlogsSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class BlogLikeView(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,*args,**kwargs):
        blog_id=kwargs.get("blog_id")
        blog=Blogs.objects.get(id=blog_id)
        blog.liked_by.add(request.user)
        total_likes=blog.liked_by.all().count()
        return Response({"likedcount":total_likes})

class BlogcommentView(APIView):
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):
        blog_id=kwargs.get("blog_id")
        blog=Blogs.objects.get(id=blog_id)
        serializer=CommentSerializer(data=request.data,context={"blog":blog,"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


# class


# class  BlogsDetailView(APIView):
#
#     def get(self,request,*args,**kwargs):
#         id=kwargs.get("blog_id")
#         detail=Blogs.objects.get(id=id)
#         serializer=BlogsSerializer(detail)
#         return Response(serializer.data)
#
#     def put(self,request,*args,**kwargs):
#         id=kwargs.get("blog_id")
#         details=Blogs.objects.get(id=id)
#         serializer=BlogsSerializer(instance=details,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#     def delete(self,request,*args,**kwargs):
#         id=kwargs.get("blog_id")
#         details=Blogs.objects.get(id=id)
#         details.delete()
#         return Response({'msg':"deleted"})

class CommentDetail(APIView):

    def get(self,request,*args,**kwargs):
        blog_id=kwargs.get("blog_id")
        comments=Comment.objects.filter(blog=blog_id)
        return Response({"data":comments})

class BlogsMixinView(GenericAPIView,
                     ListModelMixin,CreateModelMixin):
    serializer_class = BlogsSerializer
    queryset = Blogs.objects.all()
    authentication_classes = [authentication.BasicAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


class ViewSetView(ModelViewSet):
    model=Blogs
    serializer_class = BlogsSerializer
    queryset = Blogs.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self,id):
        return Blogs.objects.get(id=id)

    def get_queryset(self):
        return Blogs.objects.filter(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer=BlogsSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    @action(["GET"],detail=True)
    def get_likes(self,request,*args,**kwargs):
        post=self.get_object()
        data=post.liked_by.all()
        serializer= UserSerializer(data,many=True)
        return Response(serializer.data)

    @action(["GET"],detail=True)
    def add_likes(self,request,*args,**kwargs):
        user=self.request.user
        post=self.get_object(kwargs.get("pk"))    #to get that specific post
        post.liked_by.add(user)
        post.save()
        return Response({"msg":"liked"})


    @action(["GET"],detail=False)
    def all_post(self,request,*args,**kwargs):
        qs=Blogs.objects.all()
        serializer=BlogsSerializer(qs,many=True)
        return Response(serializer.data)


    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        blog=Blogs.objects.get(id=id)
        serializer=BlogsSerializer(blog)
        return Response(serializer.data)
