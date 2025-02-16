from django.urls import path

from.views import PostView, PostListView, CommentView, LikeView, CommentReplayView, UserView, LikeCommentView

urlpatterns = [
    path('post/', PostView.as_view(), name='post'),
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    path('post-list/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/comments/', CommentView.as_view(), name='comment'),
    path('post/<int:pk>/likes/', LikeView.as_view(), name='like'),
    #path('post/<int:pk>/comments/<int:pk>/', CommentReplayView.as_view(), name='comment-replay'),
    path('comments/<int:pk>/replay/', CommentReplayView.as_view(), name='comment-replay'),
    path('user-comments/', UserView.as_view(), name='user-comment'),
    path('comments/<int:pk>/likes/', LikeCommentView.as_view(), name='like-comment'),
]