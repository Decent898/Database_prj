from django.contrib import admin
from .models import Signature

@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at', 'is_public']
    list_filter = ['is_public', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    date_hierarchy = 'created_at'
