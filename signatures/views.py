from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
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
        
class SignatureBoardView(ListView):
    """显示互动式签名墙"""
    model = Signature
    template_name = 'signatures/signature_board.html'
    context_object_name = 'signatures'
    
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
            # 表单的save方法中已处理位置和角度
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

@login_required
@require_POST
def save_signature_positions(request):
    """保存签名位置、角度和大小的AJAX端点"""
    try:
        data = json.loads(request.body)
        positions = data.get('positions', [])
        
        for pos in positions:
            signature_id = pos.get('id')
            signature = Signature.objects.get(id=signature_id)
            
            # 验证权限 - 允许管理员或创建该签名的用户更新位置
            if request.user.is_staff or signature.user == request.user:
                signature.position_x = pos.get('position_x', 0)
                signature.position_y = pos.get('position_y', 0)
                signature.rotation = pos.get('rotation', 0)
                signature.scale = pos.get('scale', 1.0)
                signature.z_index = pos.get('z_index', 1)
                signature.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
        
def toggle_signature_visibility(request, pk):
    """切换签名在墙上的可见性"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': '请先登录'})
        
    try:
        data = json.loads(request.body)
        visibility = data.get('is_public', True)
        
        signature = Signature.objects.get(pk=pk)
        
        # 权限检查 - 只有自己或管理员才能修改
        if request.user.is_staff or signature.user == request.user:
            signature.is_public = visibility
            signature.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': '您没有权限修改此签名'})
    except Signature.DoesNotExist:
        return JsonResponse({'success': False, 'error': '签名不存在'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def get_my_signatures(request):
    """获取当前用户的所有签名，用于侧边栏显示"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': '请先登录'})
    
    try:
        # 获取所有签名，包括公开和非公开的
        signatures = Signature.objects.filter(user=request.user).order_by('-created_at')
        
        # 记录获取到的签名数量以便调试
        signature_count = signatures.count()
        print(f"【调试】为用户 {request.user.username} 获取到 {signature_count} 个签名")
        
        # 获取当前在签名墙上显示的签名ID列表
        on_board_signatures = Signature.objects.filter(user=request.user, is_public=True).values_list('id', flat=True)
        
        # 准备签名数据
        signatures_data = []
        for signature in signatures:
            try:
                # 确保图片URL存在
                image_url = signature.image.url if signature.image else None
                
                signatures_data.append({
                    'id': signature.id,
                    'title': signature.title,
                    'image_url': image_url,
                    'is_public': signature.is_public,
                    'on_board': signature.id in on_board_signatures,
                    'position_x': signature.position_x,
                    'position_y': signature.position_y,
                    'rotation': signature.rotation,
                    'scale': signature.scale,
                    'z_index': signature.z_index
                })
            except Exception as item_err:
                # 处理单个签名的错误，但不中断整个过程
                print(f"【警告】处理签名 ID:{signature.id} 时出错: {str(item_err)}")
        
        # 返回成功结果
        return JsonResponse({
            'success': True, 
            'signatures': signatures_data,
            'count': len(signatures_data)
        })
    except Exception as e:
        # 记录详细错误信息以便调试
        import traceback
        print(f"【错误】获取签名时出现异常: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({'success': False, 'error': str(e)})
