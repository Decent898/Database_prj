from django.shortcuts import render
from signatures.models import Signature, SignaturePlacement
from blog.models import Post
from django.contrib.auth.models import User

def home_view(request):
    """
    显示网站首页，包括最新签名和最新博客文章以及统计数据
    """
    # 获取在任何板上可见的最新4个签名
    # 我们通过查询 is_public=True 的 SignaturePlacement 来找到所有可见的签名
    # 然后获取这些签名，并按创建日期排序，同时使用 distinct() 确保唯一性
    visible_placements = SignaturePlacement.objects.filter(is_public=True)
    latest_signatures = Signature.objects.filter(
        signatureplacement__in=visible_placements
    ).distinct().order_by('-created_at')[:4]
    
    # 获取最新的4个已发布博客文章
    latest_posts = Post.objects.filter(is_published=True).order_by('-published_date')[:4]
    
    # 获取统计数据
    # 统计在至少一个板上可见的签名总数
    signature_count = Signature.objects.filter(signatureplacement__in=visible_placements).distinct().count()
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
