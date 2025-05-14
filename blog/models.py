from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.html import mark_safe
import markdown

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """在保存前确保slug非空，支持中文转拼音"""
        if not self.slug:
            from django.utils.text import slugify
            # 尝试将名称转换为slug
            self.slug = slugify(self.name)
            
            # 如果中文名称生成的slug为空，使用拼音转换
            if not self.slug:
                try:
                    # 使用pypinyin转换中文为拼音
                    from pypinyin import pinyin, Style
                    
                    # 获取中文拼音并组合成字符串
                    pinyin_list = pinyin(self.name, style=Style.NORMAL)
                    pinyin_str = '-'.join([''.join(item) for item in pinyin_list])
                    
                    # 生成slug，移除非ASCII字符并转为小写
                    self.slug = slugify(pinyin_str)
                    
                    # 如果拼音转换后仍为空（极少情况），使用UUID作为备选
                    if not self.slug:
                        import uuid
                        self.slug = f"tag-{uuid.uuid4().hex[:8]}"
                        
                except ImportError:
                    # 如果pypinyin未安装，使用UUID
                    import uuid
                    self.slug = f"tag-{uuid.uuid4().hex[:8]}"
            
        super().save(*args, **kwargs)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='published_date')
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=True, help_text='设置为公开以在博客中显示')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    signature = models.ForeignKey('signatures.Signature', on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    
    class Meta:
        ordering = ['-published_date']
    
    def publish(self):
        self.published_date = timezone.now()
        self.is_published = True
        self.save()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk, 'slug': self.slug})
    
    def get_content_as_html(self):
        """将Markdown内容转换为HTML，支持LaTeX数学公式"""
        # 准备标准扩展
        extensions = [
            'markdown.extensions.fenced_code', 
            'markdown.extensions.tables', 
            'markdown.extensions.toc',
        ]
        
        # 准备扩展配置
        extension_configs = {}
        
        # 尝试添加数学公式扩展
        try:
            import mdx_math
            extensions.append('mdx_math')
            extension_configs['mdx_math'] = {
                'enable_dollar_delimiter': True,  # 启用$单个美元符号作为行内公式标记
                'add_preview': True              # 添加数学公式预览
            }
        except ImportError:
            # 如果未安装mdx_math，只打印警告而不中断渲染
            print("警告: python-markdown-math未安装，数学公式可能无法正确渲染")
            
        # 处理Markdown
        html = markdown.markdown(
            self.content,
            extensions=extensions,
            extension_configs=extension_configs
        )
        return mark_safe(html)
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created_date']
    
    def __str__(self):
        return f"{self.author.username}对《{self.post.title}》的评论"
