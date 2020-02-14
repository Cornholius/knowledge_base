from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostNewView.as_view(), name='post_new'),
    path('tag/<tag_slug>', views.PostListView.as_view(), name='post_list_by_tag')
]
