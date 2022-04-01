from django.urls import path
from feed.views import *

urlpatterns = [
    path('feed/', PostList.as_view(), name='post-list'),
    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/create/', PostCreate.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),

    path('posts/<int:pk>/replies/', ReplyList.as_view(), name='replies'),
    path('replies/<int:pk>/', ReplyDetail.as_view(), name='reply-detail'),
    
    path('posts/<int:pk>/vote/<str:action>/', VotePost.as_view(), name='vote'),
    path('posts/<int:pk>/vote/remove/', RemoveVote.as_view(), name='vote-remove'),
]