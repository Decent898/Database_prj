from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Signature
from .forms import SignatureForm

class SignatureListView(ListView):
    """显示所有公开的签名"""
    model = Signature
    template_name = 'signatures/signature_list.html'
    context_object_name = 'signatures'
    paginate_by = 12
    
    def get_queryset(self):
        return Signature.objects.filter(is_public=True)

class UserSignatureListView(ListView):
    """显示特定用户的所有公开签名"""
    model = Signature
    template_name = 'signatures/user_signatures.html'
    context_object_name = 'signatures'
    paginate_by = 12
    
    def get_queryset(self):
        username = self.kwargs.get('username')
        return Signature.objects.filter(user__username=username, is_public=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs.get('username')
        return context

class SignatureDetailView(DetailView):
    """单个签名详情页面"""
    model = Signature
    template_name = 'signatures/signature_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 获取相关博客文章
        context['related_posts'] = self.object.posts.filter(is_published=True)[:5]
        return context

@login_required
def create_signature(request):
    """创建新签名"""
    if request.method == 'POST':
        form = SignatureForm(request.POST, request.FILES)
        if form.is_valid():
            signature = form.save(commit=False)
            signature.user = request.user
            signature.save()
            messages.success(request, '您的签名已成功上传！')
            return redirect('signature_detail', pk=signature.pk)
    else:
        form = SignatureForm()
    
    return render(request, 'signatures/signature_form.html', {'form': form})

class SignatureUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """更新签名"""
    model = Signature
    form_class = SignatureForm
    template_name = 'signatures/signature_form.html'
    
    def test_func(self):
        signature = self.get_object()
        return self.request.user == signature.user

class SignatureDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """删除签名"""
    model = Signature
    template_name = 'signatures/signature_confirm_delete.html'
    success_url = reverse_lazy('my_signatures')
    
    def test_func(self):
        signature = self.get_object()
        return self.request.user == signature.user

@login_required
def my_signatures(request):
    """显示当前用户的所有签名"""
    signatures = Signature.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'signatures/my_signatures.html', {'signatures': signatures})
