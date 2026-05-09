from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'completed', 'created', 'due_date']
    list_filter = ['completed', 'created', 'due_date']
    search_fields = ['title', 'description']
    list_editable = ['completed']
    list_per_page = 20
    date_hierarchy = 'created'
    
    fieldsets = (
        ('معلومات المهمة', {
            'fields': ('title', 'description', 'completed')
        }),
        ('التواريخ', {
            'fields': ('due_date', 'created', 'updated'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created', 'updated')