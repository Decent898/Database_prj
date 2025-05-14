from django import forms
from .models import Signature

class SignatureForm(forms.ModelForm):
    # 添加旋转角度选择
    ROTATION_CHOICES = [
        (0, '正向 (0°)'),
        (-15, '轻微向左 (-15°)'),
        (15, '轻微向右 (15°)'),
        (-30, '向左倾斜 (-30°)'),
        (30, '向右倾斜 (30°)'),
        (180, '上下翻转 (180°)'),
    ]
    
    initial_rotation = forms.ChoiceField(
        choices=ROTATION_CHOICES, 
        initial=0,
        label='初始角度',
        help_text='您可以在签名墙上随时调整角度'
    )
    
    class Meta:
        model = Signature
        fields = ['title', 'image', 'description', 'is_public', 'initial_rotation']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '签名的标题'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': '对您的签名进行简短描述'}),
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # 设置随机的初始位置
        import random
        instance.position_x = random.randint(50, 500) 
        instance.position_y = random.randint(50, 400)
        instance.rotation = int(self.cleaned_data.get('initial_rotation', 0))
        
        if commit:
            instance.save()
        return instance
