from django import forms
from .models import Signature

class SignatureForm(forms.ModelForm):
    # 已移除初始角度选择，上传后可在签名墙上自由调整角度
    
    class Meta:
        model = Signature
        fields = ['title', 'image', 'description', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '签名的标题', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': '对您的签名进行简短描述', 'class': 'form-control'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 当使用canvas时，image字段不是必需的
        self.fields['image'].required = False
    
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
