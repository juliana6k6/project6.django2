from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import (PostCreateView, PostDeleteView, PostDetailView,
                        PostListView, PostUpdateView)

app_name = BlogConfig.name


urlpatterns = [

    path("postdetails/<int:pk>/", PostDetailView.as_view(), name="post_details"),
    path("postcreate/", PostCreateView.as_view(), name="post_create"),
    path("postupdate/<int:pk>/", PostUpdateView.as_view(), name="post_update"),
    path("postdelete/<int:pk>/", PostDeleteView.as_view(), name="post_delete"),
    path("", PostListView.as_view(), name="post_list")]
    # path("", cache_page(60)(PostListView.as_view()), name="post_list")]
