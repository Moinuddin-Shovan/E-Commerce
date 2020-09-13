from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="forumHome"),
    path("blogPost/<int:post_id>", views.blog_post, name="forumPost")

]
