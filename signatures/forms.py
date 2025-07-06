from django import forms
from .models import Signature, SignatureBoard

class SignatureBoardForm(forms.ModelForm):
    """创建和编辑签名墙的表单"""
    class Meta:
        model = SignatureBoard
        fields = ['title', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '签名墙标题', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': '签名墙描述', 'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SignatureForm(forms.ModelForm):
    """上传和编辑签名的表单"""
    
    class Meta:
        model = Signature
        fields = ['title', 'image', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '签名的标题', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': '对您的签名进行简短描述', 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        # user 参数不再需要，但为了兼容可能存在的调用，先移除
        kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # 当使用canvas绘制签名时，图片上传不是必需的
        self.fields['image'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        
        # 视图(view)中会进一步检查，确保 image 或 canvas_data 至少有一个存在
        if not image:
            pass
        
        return cleaned_data
