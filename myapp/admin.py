from django.contrib import admin
from .models import Theme, ThemeVariable


class ThemeVariableInline(admin.TabularInline):
    model = ThemeVariable
    extra = 5
    fields = ['name', 'value']


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'identifier', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'identifier']
    inlines = [ThemeVariableInline]
    actions = ['activate_theme']
    
    def activate_theme(self, request, queryset):
        """批量激活主题（只激活最后一个选中的）"""
        Theme.objects.filter(is_active=True).update(is_active=False)
        
        if queryset.exists():
            last_theme = queryset.last()
            last_theme.is_active = True
            last_theme.save()
            
            self.message_user(request, f"已激活 {last_theme.name} 主题")
    activate_theme.short_description = "激活选中的主题"


@admin.register(ThemeVariable)
class ThemeVariableAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'theme']
    list_filter = ['theme']
    search_fields = ['name', 'value', 'theme__name']