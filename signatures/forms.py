from django import forms
from .models import Signature

class SignatureForm(forms.ModelForm):
    class Meta:
        model = Signature
        fields = ['title', 'image', 'description', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': '签名的标题'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': '对您的签名进行简短描述'}),
        }
