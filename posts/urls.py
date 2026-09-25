from django.urls import path
from .views import PostListCreateView, PostDeleteView, LikeToggleView, CommentListCreateView, UserPostListView

urlpatterns = [
    path('',                   PostListCreateView.as_view(),    name='post-list-create'),
    path('<int:pk>/',          PostDeleteView.as_view(),        name='post-delete'),
    path('<int:pk>/like/',     LikeToggleView.as_view(),        name='post-like'),
    path('<int:pk>/comments/', CommentListCreateView.as_view(), name='post-comments'),
    path('mine/',              UserPostListView.as_view(),      name='my-posts'), 
]