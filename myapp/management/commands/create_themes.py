from django.core.management.base import BaseCommand
from myapp.models import Theme, ThemeVariable


class Command(BaseCommand):
    help = '创建初始主题数据'

    def handle(self, *args, **options):
        light_theme, created = Theme.objects.get_or_create(
            name='浅色主题',
            identifier='light',
            defaults={
                'is_active': True
            }
        )
        
        if created:
            light_variables = {
                'primary': '#007bff',
                'secondary': '#6c757d',
                'background': '#ffffff',
                'text': '#212529',
                'border': '#dee2e6',
                'shadow': 'rgba(0, 0, 0, 0.1)',
                'card-bg': '#ffffff',
                'navbar-bg': '#f8f9fa',
                'navbar-text': '#212529',
                'footer-bg': '#f8f9fa',
                'footer-text': '#212529',
            }
            
            for name, value in light_variables.items():
                ThemeVariable.objects.get_or_create(
                    theme=light_theme,
                    name=name,
                    defaults={'value': value}
                )
            
            self.stdout.write(self.style.SUCCESS('浅色主题创建成功'))
        
        dark_theme, created = Theme.objects.get_or_create(
            name='暗色主题',
            identifier='dark',
            defaults={
                'is_active': False
            }
        )
        
        if created:
            dark_variables = {
                'primary': '#0d6efd',
                'secondary': '#6c757d',
                'background': '#121212',
                'text': '#ffffff',
                'border': '#404040',
                'shadow': 'rgba(0, 0, 0, 0.3)',
                'card-bg': '#1e1e1e',
                'navbar-bg': '#343a40',
                'navbar-text': '#ffffff',
                'footer-bg': '#343a40',
                'footer-text': '#ffffff',
            }
            
            for name, value in dark_variables.items():
                ThemeVariable.objects.get_or_create(
                    theme=dark_theme,
                    name=name,
                    defaults={'value': value}
                )
            
            self.stdout.write(self.style.SUCCESS('暗色主题创建成功'))
        
        blue_theme, created = Theme.objects.get_or_create(
            name='蓝色主题',
            identifier='blue',
            defaults={
                'is_active': False
            }
        )
        
        if created:
            blue_variables = {
                'primary': '#0056b3',
                'secondary': '#6c757d',
                'background': '#f8faff',
                'text': '#212529',
                'border': '#b3d7ff',
                'shadow': 'rgba(0, 86, 179, 0.1)',
                'card-bg': '#ffffff',
                'navbar-bg': '#0056b3',
                'navbar-text': '#ffffff',
                'footer-bg': '#e6f2ff',
                'footer-text': '#212529',
            }
            
            for name, value in blue_variables.items():
                ThemeVariable.objects.get_or_create(
                    theme=blue_theme,
                    name=name,
                    defaults={'value': value}
                )
            
            self.stdout.write(self.style.SUCCESS('蓝色主题创建成功'))
        
        green_theme, created = Theme.objects.get_or_create(
            name='绿色主题',
            identifier='green',
            defaults={
                'is_active': False
            }
        )
        
        if created:
            green_variables = {
                'primary': '#28a745',
                'secondary': '#6c757d',
                'background': '#f8fff9',
                'text': '#212529',
                'border': '#c3e6cb',
                'shadow': 'rgba(40, 167, 69, 0.1)',
                'card-bg': '#ffffff',
                'navbar-bg': '#28a745',
                'navbar-text': '#ffffff',
                'footer-bg': '#e6f7ec',
                'footer-text': '#212529',
            }
            
            for name, value in green_variables.items():
                ThemeVariable.objects.get_or_create(
                    theme=green_theme,
                    name=name,
                    defaults={'value': value}
                )
            
            self.stdout.write(self.style.SUCCESS('绿色主题创建成功'))
        
        self.stdout.write(self.style.SUCCESS('所有初始主题数据创建完成'))