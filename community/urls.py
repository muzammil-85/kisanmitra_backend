from django.urls import path
from .views import AddCommentToPost, CommunityPostWithImageView, ListCommunityPosts

urlpatterns = [
    path('community/post/', CommunityPostWithImageView.as_view(), name='community-post-image'),
     path('community/post/<str:post_id>/comment/', AddCommentToPost.as_view(), name='add-comment'),
     path('community/list-posts/', ListCommunityPosts.as_view(), name='list-community-posts'),
]
