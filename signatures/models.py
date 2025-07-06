from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class SignatureBoard(models.Model):
    """签名墙模型"""
    title = models.CharField(max_length=100, verbose_name="标题")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signature_boards', verbose_name="创建者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    # 通过 SignaturePlacement 建立多对多关系
    signatures = models.ManyToManyField('Signature', through='SignaturePlacement', related_name='boards', verbose_name="签名")

    def __str__(self):
        return self.title

class Signature(models.Model):
    """签名模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    title = models.CharField(max_length=100, verbose_name="标题")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    image = models.ImageField(upload_to='signatures/', verbose_name="签名图片")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # is_public 字段移至 SignaturePlacement

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class SignaturePlacement(models.Model):
    """签名在特定墙上的位置和状态"""
    signature = models.ForeignKey(Signature, on_delete=models.CASCADE, verbose_name="签名")
    board = models.ForeignKey(SignatureBoard, on_delete=models.CASCADE, verbose_name="签名墙")
    
    position_x = models.FloatField(default=0, verbose_name="X坐标")
    position_y = models.FloatField(default=0, verbose_name="Y坐标")
    rotation = models.FloatField(default=0, verbose_name="旋转角度")
    scale = models.FloatField(default=1.0, verbose_name="缩放比例")
    z_index = models.IntegerField(default=1, verbose_name="层级")
    is_public = models.BooleanField(default=True, verbose_name="是否在墙上显示")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        # 确保一个签名在一个墙上只有一个位置记录
        unique_together = ('signature', 'board')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.signature.title} on {self.board.title}"
