from django.contrib import admin
from .models import Plan
# Register your models here.


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_by', 'created_at']
    list_filter = ['created_by', 'created_at']
    search_fields = ['title', 'desciption']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'desciption')
        }),
        ('اطلاعات تکمیلی', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )