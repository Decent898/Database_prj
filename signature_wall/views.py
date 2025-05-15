from django.shortcuts import render
from signatures.models import Signature
from blog.models import Post
from django.contrib.auth.models import User

def home_view(request):
    """
    显示网站首页，包括最新签名和最新博客文章以及统计数据
    """
    # 获取最新的4个公开签名
    latest_signatures = Signature.objects.filter(is_public=True).order_by('-created_at')[:4]
    
    # 获取最新的4个已发布博客文章
    latest_posts = Post.objects.filter(is_published=True).order_by('-published_date')[:4]
    
    # 获取统计数据
    signature_count = Signature.objects.filter(is_public=True).count()
    post_count = Post.objects.filter(is_published=True).count()
    user_count = User.objects.count()
    
    context = {
        'latest_signatures': latest_signatures,
        'latest_posts': latest_posts,
        'signature_count': signature_count,
        'post_count': post_count,
        'user_count': user_count
    }
    
    return render(request, 'home.html', context)
