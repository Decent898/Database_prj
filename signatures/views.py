from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import json
from .models import Signature, SignatureBoard, SignaturePlacement
from .forms import SignatureForm, SignatureBoardForm

# ===== 签名墙相关视图 =====

class SignatureBoardListView(ListView):
    """显示所有签名墙"""
    model = SignatureBoard
    template_name = 'signatures/board_list.html'
    context_object_name = 'boards'
    paginate_by = 9
    
    def get_queryset(self):
        return SignatureBoard.objects.filter(is_active=True)

class SignatureBoardDetailView(DetailView):
    """显示特定签名墙的互动式界面"""
    model = SignatureBoard
    template_name = 'signatures/signature_board.html'
    context_object_name = 'board'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 通过SignaturePlacement获取属于该签名墙的所有可见签名及其位置信息
        placements = SignaturePlacement.objects.filter(
            board=self.object,
            is_public=True  # 修正：使用 is_public 字段
        ).select_related('signature', 'signature__user')

        # 传递placements给模板，模板将从中获取签名和位置信息
        context['placements'] = placements
        # 为了向后兼容或简化模板逻辑，可以保留一个signatures列表
        context['signatures'] = [p.signature for p in placements]
        return context

@login_required
def create_signature_board(request):
    """创建新的签名墙"""
    if request.method == 'POST':
        form = SignatureBoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.created_by = request.user
            board.save()
            messages.success(request, '签名墙创建成功！')
            return redirect('signature_board_detail', pk=board.pk)
    else:
        form = SignatureBoardForm()
    
    return render(request, 'signatures/board_form.html', {'form': form})

class SignatureBoardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """更新签名墙"""
    model = SignatureBoard
    form_class = SignatureBoardForm
    template_name = 'signatures/board_form.html'
    
    def test_func(self):
        board = self.get_object()
        return self.request.user == board.created_by

class SignatureBoardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """删除签名墙"""
    model = SignatureBoard
    template_name = 'signatures/board_confirm_delete.html'
    success_url = reverse_lazy('my_signature_boards')
    
    def test_func(self):
        board = self.get_object()
        return self.request.user == board.created_by

@login_required
def my_signature_boards(request):
    """显示当前用户的所有签名墙"""
    boards = SignatureBoard.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'signatures/my_boards.html', {'boards': boards})

# ===== 签名相关视图 ====

class SignatureListView(ListView):
    """显示所有公开的签名"""
    model = Signature
    template_name = 'signatures/signature_list.html'
    context_object_name = 'signatures'
    paginate_by = 12
    
    def get_queryset(self):
        return Signature.objects.filter(is_public=True)
        
class SignatureBoardView(ListView):
    """显示默认互动式签名墙（向后兼容）"""
    model = Signature
    template_name = 'signatures/signature_board.html'
    context_object_name = 'signatures'
    
    def get_queryset(self):
        # 返回没有指定board的公开签名（兼容旧数据）
        return Signature.objects.filter(is_public=True, board__isnull=True)

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
    
    # 移除了 get_context_data, 因为 related_posts 不再存在

class SignatureUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """更新签名"""
    model = Signature
    form_class = SignatureForm
    template_name = 'signatures/signature_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
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
def create_signature(request, board_id=None):
    """创建新签名，并可选择性地关联到特定签名墙"""
    board = None
    if board_id:
        board = get_object_or_404(SignatureBoard, pk=board_id)

    if request.method == 'POST':
        form = SignatureForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            signature = form.save(commit=False)
            signature.user = request.user
            signature.save()
            
            # 如果有关联的签名墙，则创建 SignaturePlacement
            if board:
                SignaturePlacement.objects.create(
                    signature=signature,
                    board=board,
                    # 可以在这里设置初始位置等
                )
                messages.success(request, f'签名已成功创建并添加到“{board.title}”墙上！')
                return redirect('signature_board_detail', pk=board.pk)
            
            messages.success(request, '签名创建成功！')
            return redirect('my_signatures')
    else:
        form = SignatureForm(user=request.user)

    return render(request, 'signatures/signature_form.html', {
        'form': form,
        'board': board
    })

@login_required
@require_POST
def save_signature_positions(request, board_id=None):
    """保存签名位置、角度和大小的AJAX端点"""
    try:
        # 确认操作的是哪个签名墙
        board = get_object_or_404(SignatureBoard, pk=board_id)
        data = json.loads(request.body)
        positions = data.get('positions', [])
        
        for pos in positions:
            signature_id = pos.get('id')
            # 找到对应的SignaturePlacement记录进行更新
            placement = get_object_or_404(SignaturePlacement, signature_id=signature_id, board=board)
            
            # 验证权限 - 允许管理员或创建该签名的用户更新位置
            if request.user.is_staff or placement.signature.user == request.user:
                placement.position_x = pos.get('position_x', 0)
                placement.position_y = pos.get('position_y', 0)
                placement.rotation = pos.get('rotation', 0)
                placement.scale = pos.get('scale', 1.0)
                placement.z_index = pos.get('z_index', 1)
                placement.save()
        
        return JsonResponse({'success': True})
    except SignatureBoard.DoesNotExist:
        return JsonResponse({'success': False, 'error': '指定的签名墙不存在。'})
    except SignaturePlacement.DoesNotExist:
        return JsonResponse({'success': False, 'error': '尝试更新一个不在此墙上的签名。'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
        
@login_required
@require_POST
def toggle_signature_visibility(request, pk):
    """切换签名在特定墙上的可见性"""
    try:
        data = json.loads(request.body)
        board_id = data.get('board_id')
        is_public = data.get('is_public') # 修正：使用 is_public

        if board_id is None or is_public is None:
            return JsonResponse({'success': False, 'error': '缺少 board_id 或 is_public 参数'}, status=400)

        board = get_object_or_404(SignatureBoard, pk=board_id)
        signature = get_object_or_404(Signature, pk=pk)

        # 权限检查 - 只有自己或管理员才能修改
        if not (request.user.is_staff or signature.user == request.user):
            return JsonResponse({'success': False, 'error': '您没有权限修改此签名'}, status=403)

        # 获取或创建placement
        placement, created = SignaturePlacement.objects.get_or_create(
            signature=signature,
            board=board
        )
        
        placement.is_public = is_public # 修正：使用 is_public
        placement.save()
        
        action = "显示" if is_public else "隐藏"
        return JsonResponse({'success': True, 'message': f'签名已成功在当前墙上{action}。'})

    except Signature.DoesNotExist:
        return JsonResponse({'success': False, 'error': '签名不存在'}, status=404)
    except SignatureBoard.DoesNotExist:
        return JsonResponse({'success': False, 'error': '签名墙不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def get_my_signatures(request):
    """获取当前用户的所有签名，并标记它们在特定墙上的状态"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': '请先登录'}, status=401)

    board_id = request.GET.get('board_id')
    if not board_id:
        return JsonResponse({'success': False, 'error': '缺少 board_id 参数'}, status=400)

    try:
        # 获取用户的所有签名
        user_signatures = Signature.objects.filter(user=request.user).order_by('-created_at')
        
        # 获取当前墙上所有相关的placement记录
        placements_on_board = SignaturePlacement.objects.filter(
            board_id=board_id, 
            signature__user=request.user
        ).values('signature_id', 'is_public')
        
        # 创建一个字典以便快速查找签名在当前板上的公开状态
        board_signature_status = {p['signature_id']: p['is_public'] for p in placements_on_board}

        signatures_data = []
        for signature in user_signatures:
            image_url = signature.image.url if signature.image else None
            # 检查签名是否存在于当前板的placement记录中
            on_board = signature.pk in board_signature_status
            # 获取其在当前板上的可见状态，如果不在板上则默认为False
            is_public_on_board = board_signature_status.get(signature.pk, False)

            signatures_data.append({
                'id': signature.pk,
                'title': signature.title,
                'image_url': image_url,
                'on_board': on_board, # 是否在当前墙上 (有placement记录)
                'is_public': is_public_on_board, # 在当前墙上是否可见
            })
        
        return JsonResponse({
            'success': True, 
            'signatures': signatures_data,
        })
    except Exception as e:
        import traceback
        print(f"【错误】获取签名时出现异常: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
