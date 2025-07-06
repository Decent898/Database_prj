from django.contrib import admin
from .models import Signature, SignatureBoard, SignaturePlacement

@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description', 'user__username']
    date_hierarchy = 'created_at'

@admin.register(SignatureBoard)
class SignatureBoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    date_hierarchy = 'created_at'

@admin.register(SignaturePlacement)
class SignaturePlacementAdmin(admin.ModelAdmin):
    list_display = ('signature', 'board', 'is_public', 'z_index')
    list_filter = ('board', 'is_public')
    search_fields = ('signature__title', 'board__title')
    autocomplete_fields = ['signature', 'board']
