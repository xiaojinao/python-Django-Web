from django.apps import AppConfig
from django.db import connection


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        """应用启动时的初始化操作"""
        from django.core.management import call_command
        import os
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'myapp_%'"
                )
                tables = [row[0] for row in cursor.fetchall()]
                
                required_tables = ['myapp_forum', 'myapp_post', 'myapp_theme', 'myapp_userprofile']
                if all(table in tables for table in required_tables):
                    if 'migrate' not in os.sys.argv:
                        call_command('create_themes')
        except Exception:
            
            pass