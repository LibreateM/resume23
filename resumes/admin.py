from django.contrib import admin
from .models import Resume

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'template', 'is_ai_generated', 'created_at']
    list_filter = ['template', 'is_ai_generated']
    search_fields = ['title', 'user__username', 'full_name']
    readonly_fields = ['created_at', 'updated_at']
