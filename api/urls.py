from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("posts",views.ViewSetView,basename="post")

urlpatterns=[
    path("blogs",views.BlogsView.as_view()),
    path("blogs/like/<int:blog_id>",views.BlogLikeView.as_view()),
    path("blogs/comments/add/<int:blog_id>",views.BlogcommentView.as_view()),
    path("blogs/comments/<int:blog_id>",views.BlogcommentView.as_view()),
    path("blogsmixin",views.BlogsMixinView.as_view())
]+router.urls