from django.urls import path
from . import views

urlpatterns = [
    # 签名墙管理
    path('boards/', views.SignatureBoardListView.as_view(), name='signature_board_list'),
    path('boards/<int:pk>/', views.SignatureBoardDetailView.as_view(), name='signature_board_detail'),
    path('boards/new/', views.create_signature_board, name='create_signature_board'),
    path('boards/<int:pk>/update/', views.SignatureBoardUpdateView.as_view(), name='update_signature_board'),
    path('boards/<int:pk>/delete/', views.SignatureBoardDeleteView.as_view(), name='delete_signature_board'),
    path('my-boards/', views.my_signature_boards, name='my_signature_boards'),
    
    # 默认签名墙（向后兼容）
    path('', views.SignatureListView.as_view(), name='signature_list'),
    path('board/', views.SignatureBoardView.as_view(), name='signature_board'),
    
    # 签名位置保存功能
    path('boards/<int:board_id>/save-positions/', views.save_signature_positions, name='save_board_positions'),
    path('save-positions/', views.save_signature_positions, name='save_signature_positions'),
    
    # 签名管理
    path('my-signatures/', views.my_signatures, name='my_signatures'),
    path('api/my-signatures/', views.get_my_signatures, name='api_my_signatures'),
    path('new/', views.create_signature, name='create_signature'),
    path('boards/<int:board_id>/new/', views.create_signature, name='create_board_signature'),
    path('<int:pk>/', views.SignatureDetailView.as_view(), name='signature_detail'),
    path('<int:pk>/update/', views.SignatureUpdateView.as_view(), name='update_signature'),
    path('<int:pk>/delete/', views.SignatureDeleteView.as_view(), name='delete_signature'),
    path('<int:pk>/toggle-visibility/', views.toggle_signature_visibility, name='toggle_signature_visibility'),
    
    # 用户签名列表
    path('user/<str:username>/', views.UserSignatureListView.as_view(), name='user_signatures'),
]
