from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, MeView,
    FollowToggleView, UserSearchView,
    ChangePasswordView,
    FollowersListView, FollowingListView,  # ← novos
)

urlpatterns = [
    path('register/',         RegisterView.as_view(),       name='register'),
    path('login/',            LoginView.as_view(),           name='login'),
    path('refresh/',          TokenRefreshView.as_view(),   name='token_refresh'),
    path('me/',               MeView.as_view(),              name='me'),
    path('<int:pk>/follow/',  FollowToggleView.as_view(),   name='follow-toggle'),
    path('search/',           UserSearchView.as_view(),     name='user-search'),
    path('change-password/',  ChangePasswordView.as_view(), name='change-password'),
    path('me/followers/',     FollowersListView.as_view(),  name='my-followers'),  # ← novo
    path('me/following/',     FollowingListView.as_view(),  name='my-following'),  # ← novo
]