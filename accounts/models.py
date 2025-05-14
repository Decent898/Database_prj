from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', default='profile_pics/default.png')
    website = models.URLField(max_length=200, blank=True)
    
    def __str__(self):
        return f"{self.user.username}的个人资料"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """当用户创建时自动创建个人资料"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """当用户更新时自动更新个人资料"""
    instance.profile.save()
