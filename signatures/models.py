from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class SignatureBoard(models.Model):
    """签名墙模型，可以创建多个签名墙"""
    title = models.CharField(max_length=100, verbose_name="标题")
    description = models.TextField(blank=True, verbose_name="描述")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signature_boards')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "签名墙"
        verbose_name_plural = "签名墙"
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('signature_board_detail', kwargs={'pk': self.pk})


class Signature(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signatures')
    board = models.ForeignKey(SignatureBoard, on_delete=models.CASCADE, related_name='signatures', null=True, blank=True)
    image = models.ImageField(upload_to='signatures', blank=True, help_text='上传您的手写签名或使用画布绘制')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=True, help_text='设置为公开以在签名墙上显示')
    
    # 动态签名墙的位置和样式属性
    position_x = models.FloatField(default=0, help_text='签名在墙上的X坐标')
    position_y = models.FloatField(default=0, help_text='签名在墙上的Y坐标')
    rotation = models.IntegerField(default=0, help_text='签名的旋转角度(0-360)')
    scale = models.FloatField(default=1.0, help_text='签名的缩放比例')
    z_index = models.IntegerField(default=1, help_text='签名的层叠顺序')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}的签名: {self.title}"
    
    def get_absolute_url(self):
        return reverse('signature_detail', kwargs={'pk': self.pk})
    
    @property
    def related_posts(self):
        """返回与该签名关联的博客文章"""
        return self.user.posts.filter(is_published=True)
