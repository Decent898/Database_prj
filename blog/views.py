from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from .models import Post, Tag, Comment
from .forms import PostForm, CommentForm
from signatures.models import Signature

class PostListView(ListView):
    """显示所有已发布的博客文章"""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-published_date')

class UserPostListView(ListView):
    """显示特定用户的所有公开文章"""
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        username = self.kwargs.get('username')
        return Post.objects.filter(user__username=username, is_published=True).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs.get('username')
        return context

class PostDetailView(DetailView):
    """博客文章详情页面"""
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 获取上下文数据
        context['form'] = CommentForm() # 添加评论表单
        return context
    
    def post(self, request, *args, **kwargs):
        """处理评论提交"""
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, '评论提交成功！')
        return redirect('post_detail', pk=post.pk, slug=post.slug)

@login_required
def create_post(request):
    """创建新博客文章"""
    if request.method == 'POST':
        form = PostForm(request.POST, user=request.user)
        
        # 输出表单数据以进行调试
        print(f"表单数据: {request.POST}")
        print(f"表单文件: {request.FILES}")
        
        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.user = request.user
                # 确保published_date字段被设置
                if post.is_published and not post.published_date:
                    post.published_date = timezone.now()
                post.save()
                
                # 保存已选择的标签
                form.save_m2m()  
                
                # 处理新标签
                new_tags = form.cleaned_data.get('new_tags', '')
                if new_tags:
                    tag_names = [t.strip() for t in new_tags.split(',') if t.strip()]
                    for tag_name in tag_names:
                        # 此处不再生成slug，让Tag模型的save方法处理
                        # 检查标签是否已存在
                        tag, created = Tag.objects.get_or_create(
                            name=tag_name
                        )
                        # 添加到文章的标签中
                        post.tags.add(tag)
                
                messages.success(request, '文章已创建成功！')
                
                # 检查是否是AJAX请求
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    from django.http import JsonResponse
                    return JsonResponse({
                        'success': True,
                        'redirect_url': reverse('post_detail', kwargs={'pk': post.pk, 'slug': post.slug})
                    })
                else:
                    return redirect('post_detail', pk=post.pk, slug=post.slug)
            except Exception as e:
                print(f"保存文章时出错: {e}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    from django.http import JsonResponse
                    return JsonResponse({'success': False, 'error': str(e)}, status=500)
                raise
        else:
            messages.error(request, '表单验证错误，请检查输入。')
            print(f"表单验证错误: {form.errors}")
            
            # AJAX请求时返回JSON错误
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                from django.http import JsonResponse
                return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
    else:
        form = PostForm(user=request.user)
    
    return render(request, 'blog/post_form.html', {'form': form})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """更新博客文章"""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        try:
            # 先保存文章基本信息
            form.instance.user = self.request.user  # 确保用户关联
            
            # 确保published_date字段被设置
            if form.instance.is_published and not form.instance.published_date:
                form.instance.published_date = timezone.now()
                
            self.object = form.save()
            
            # 处理新标签
            new_tags = form.cleaned_data.get('new_tags', '')
            if new_tags:
                tag_names = [t.strip() for t in new_tags.split(',') if t.strip()]
                for tag_name in tag_names:
                    # 此处不再生成slug，让Tag模型的save方法处理
                    # 检查标签是否已存在
                    tag, created = Tag.objects.get_or_create(
                        name=tag_name
                    )
                    # 添加到文章的标签中
                    self.object.tags.add(tag)
            
            # 检查是否是AJAX请求
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                from django.http import JsonResponse
                return JsonResponse({
                    'success': True,
                    'redirect_url': self.get_success_url()
                })
            
            return redirect(self.get_success_url())
            
        except Exception as e:
            print(f"更新文章时出错: {e}")
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                from django.http import JsonResponse
                return JsonResponse({'success': False, 'error': str(e)}, status=500)
            raise
    
    def form_invalid(self, form):
        """处理表单验证失败情况"""
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.http import JsonResponse
            return JsonResponse({'success': False, 'errors': form.errors.as_json()}, status=400)
        return super().form_invalid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """删除博客文章"""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('my_posts')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user

@login_required
def my_posts(request):
    """显示当前用户的所有文章"""
    posts = Post.objects.filter(user=request.user).order_by('-created_date')
    return render(request, 'blog/my_posts.html', {'posts': posts})

class TagPostListView(ListView):
    """按标签分类显示文章"""
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.objects.filter(tags=tag, is_published=True).order_by('-published_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get('tag_slug')
        context['tag'] = get_object_or_404(Tag, slug=tag_slug)
        return context

def signature_posts(request, signature_id):
    """显示与特定签名相关的文章"""
    signature = get_object_or_404(Signature, id=signature_id)
    posts = Post.objects.filter(signature=signature, is_published=True).order_by('-published_date')
    return render(request, 'blog/signature_posts.html', {
        'signature': signature,
        'posts': posts
    })
