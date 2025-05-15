"""
URL configuration for signature_wall project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 首页
    path('', views.home_view, name='home'),
    
    # 账户应用URLs - 先包含自定义URLs，后包含Django内置认证URLs
    path('accounts/', include('accounts.urls')),
    # 如果'accounts.urls'中没有匹配的URL，将回退到Django内置认证视图
    path('accounts/', include('django.contrib.auth.urls')),  # Django内置认证视图
    
    # 签名墙应用URLs
    path('signatures/', include('signatures.urls')),
    
    # 博客应用URLs
    path('blog/', include('blog.urls')),
]

# 在开发环境中提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
