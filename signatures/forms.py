from django import forms
from django.db.models import Q
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
    # 已移除初始角度选择，上传后可在签名墙上自由调整角度
    
    class Meta:
        model = Signature
        fields = ['title', 'image', 'description', 'is_public', 'board']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '签名的标题', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': '对您的签名进行简短描述', 'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'board': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # 当使用canvas时，image字段不是必需的
        self.fields['image'].required = False
        # 签名墙选择不是必需的
        self.fields['board'].required = False
        # 如果是ModelChoiceField类型的字段，才可以设置empty_label和queryset
        if isinstance(self.fields['board'], forms.ModelChoiceField):
            self.fields['board'].empty_label = "请选择签名墙(可选)"
            
            # 如果提供了用户，则只显示该用户创建的签名墙
            if user:
                self.fields['board'].queryset = SignatureBoard.objects.filter(
                    Q(created_by=user) | Q(is_active=True)
                )
    
    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        
        # 检查是否有canvas数据（这将在视图中处理）
        # 如果没有image也没有canvas数据，则抛出验证错误
        if not image:
            # 这个检查将在视图中进行，因为canvas_data不在表单字段中
            pass
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # 设置随机的初始位置和角度
        import random
        instance.position_x = random.randint(50, 500) 
        instance.position_y = random.randint(50, 400)
        # 随机生成一个旋转角度，使签名墙看起来更自然
        instance.rotation = random.choice([0, -15, 15, -5, 5, -10, 10])
        
        if commit:
            instance.save()
        return instance
