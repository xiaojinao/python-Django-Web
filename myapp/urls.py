from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('', views.index, name='index'),
    path('themes/', views.theme_list, name='theme_list'),
    path('themes/create/', views.create_theme, name='create_theme'),
    path('themes/edit/<int:theme_id>/', views.edit_theme, name='edit_theme'),
    path('themes/delete/<int:theme_id>/', views.delete_theme, name='delete_theme'),
    path('themes/switch/<int:theme_id>/', views.switch_theme, name='switch_theme'),
    path('api/theme-variables/', views.get_theme_variables, name='get_theme_variables'),
    
    # ==================== 论坛功能路由 ====================
    path('forum/', views.forum_index, name='forum_index'),
    path('forum/<int:forum_id>/', views.forum_detail, name='forum_detail'),
    path('forum/<int:forum_id>/create/', views.post_create, name='post_create'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:post_id>/reply/', views.add_reply, name='add_reply'),
    path('reply/<int:reply_id>/delete/', views.delete_reply, name='delete_reply'),
    path('user/profile/', views.user_profile, name='user_profile'),
    path('user/profile/<str:username>/', views.user_profile, name='user_profile_detail'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('post/<int:post_id>/essence/', views.toggle_essence, name='toggle_essence'),
    path('post/<int:post_id>/top/', views.toggle_top, name='toggle_top'),
    
    # ==================== 用户认证路由 ====================
    # 使用自定义表单的登录视图
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),
    
    # 退出登录视图
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # 用户注册视图
    path('accounts/signup/', views.signup, name='signup'),
]