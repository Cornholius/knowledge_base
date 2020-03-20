from django.urls import path
from . import views
#   добавляем для работы медиа файлов при отключенном дебаге
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('edit/<int:pk>/', views.EditPostView.as_view(), name='post_edit'),
    path('post/new/', views.PostNewView.as_view(), name='post_new'),
    path('tag/<tag_slug>', views.PostListView.as_view(), name='post_list_by_tag')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   #добавляем для работы медиа
                                                                    # файлов при отключенном дебаге

