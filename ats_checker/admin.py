from django.contrib import admin
from .models import ATSCheck

@admin.register(ATSCheck)
class ATSCheckAdmin(admin.ModelAdmin):
    list_display = ['user', 'score', 'score_label', 'created_at']
    list_filter = ['score']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
