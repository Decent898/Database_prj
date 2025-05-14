from django.urls import path
from . import views

urlpatterns = [
    # 签名墙列表
    path('', views.SignatureListView.as_view(), name='signature_list'),
    
    # 动态交互式签名墙
    path('board/', views.SignatureBoardView.as_view(), name='signature_board'),
    path('save-positions/', views.save_signature_positions, name='save_signature_positions'),
    
    # 个人签名管理
    path('my-signatures/', views.my_signatures, name='my_signatures'),
    path('api/my-signatures/', views.get_my_signatures, name='api_my_signatures'),
    path('new/', views.create_signature, name='create_signature'),
    path('<int:pk>/', views.SignatureDetailView.as_view(), name='signature_detail'),
    path('<int:pk>/update/', views.SignatureUpdateView.as_view(), name='update_signature'),
    path('<int:pk>/delete/', views.SignatureDeleteView.as_view(), name='delete_signature'),
    path('<int:pk>/toggle-visibility/', views.toggle_signature_visibility, name='toggle_signature_visibility'),
    
    # 用户签名列表
    path('user/<str:username>/', views.UserSignatureListView.as_view(), name='user_signatures'),
]
