from django import forms
from .models import Post, Comment, Tag
from signatures.models import Signature

class PostForm(forms.ModelForm):
    # 明确指定必填字段
    title = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '文章标题'})
    )
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'rows': 15, 
            'placeholder': '# 使用Markdown格式\n\n## 二级标题\n\n- 列表项\n- 另一个列表项\n\n**粗体** *斜体* [链接](https://example.com)\n\n```python\n# 代码块\nprint("Hello, World!")\n```'
        }),
        error_messages={'required': '请输入文章内容'}
    )
    
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    new_tags = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={
            'placeholder': '添加新标签，用逗号分隔',
            'class': 'form-control'
        }),
        help_text='添加不在列表中的新标签，多个标签用逗号分隔'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'slug', 'tags', 'new_tags', 'signature', 'is_published']
        widgets = {
            # title和content已在类属性中定义
            'slug': forms.TextInput(attrs={'placeholder': '用于URL的英文标识，例如：my-first-post'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['signature'].queryset = Signature.objects.filter(user=user)
        
        # 设置 is_published 默认为选中状态
        self.fields['is_published'].initial = True
        self.fields['is_published'].widget.attrs.update({
            'checked': 'checked',
            'help_text': '默认公开文章，取消勾选将保存为草稿'
        })

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': '写下你的评论...'}),
        }
