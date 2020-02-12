from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('test/', views.post_list_test, name='post_list_new'),
    # path('tag/<tag_slug>', views.post_list, name='post_list_by_tag')
    path('tag/<tag_slug>', views.post_list, name='post_list_by_tag')
]