from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# 注意：信号接收器已经在 models.py 中定义，这个文件仅用于 AppConfig 中的 ready() 方法引用
# 避免重复定义信号接收器，否则会导致 Profile 创建两次
