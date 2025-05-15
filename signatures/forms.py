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
