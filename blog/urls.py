from django.urls import path
from blog.views import PostListView, PostCreateView, PostUpdateView, PostDeleteView, PostDetailView
from django.views.decorators.cache import cache_page
from django.conf.urls.static import static
from django.conf import settings


app_name = 'blog'


urlpatterns = [path('', cache_page(60)(PostListView.as_view()), name='post_list'),
               path('postdetails/<int:pk>/', PostDetailView.as_view(), name='post_details'),
               path('postcreate/', PostCreateView.as_view(), name='post_create'),
               path('postupdate/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
               path('postdelete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),

     ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
