from django.urls import path
from . import views

urlpatterns = [
    # 博客文章列表
    path('', views.PostListView.as_view(), name='post_list'),
    
    # 个人博客文章管理
    path('my-posts/', views.my_posts, name='my_posts'),
    path('new/', views.create_post, name='create_post'),
    path('<int:pk>/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:pk>/<slug:slug>/update/', views.PostUpdateView.as_view(), name='update_post'),
    path('<int:pk>/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
    
    # 用户文章列表
    path('user/<str:username>/', views.UserPostListView.as_view(), name='user_posts'),
    
    # 标签文章列表
    path('tag/<slug:tag_slug>/', views.TagPostListView.as_view(), name='tag_posts'),
    
    # 签名相关文章
    path('signature/<int:signature_id>/', views.signature_posts, name='signature_posts'),
]
