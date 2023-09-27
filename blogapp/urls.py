from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', about, name='blog-about'),
    path('search/', search_feature, name='search-view'),
    path('post-like/<int:pk>', PostLike, name="post-like"),
    path('postComment/<int:post_id>',add_comment, name='add-comment'),
    path('tag/<slug:tag_slug>/',post_list, name='post-tag'),
    path('add_to_saved/<int:post_id>',add_to_saved, name='add_to_saved'),
    path('saved/',show_saved_post, name='show_saved_post'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)