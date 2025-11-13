from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from .models import Theme, ThemeVariable, Forum, Post, Reply, UserProfile, Notification
from .forms import CustomUserCreationForm, UserProfileForm, UserEditForm
from django.contrib.auth.models import User


def index(request):
    active_theme = Theme.objects.filter(is_active=True).first()
    theme_variables = {}
    
    if active_theme:
        variables = active_theme.variables.all()
        theme_variables = {var.name: var.value for var in variables}
    
    context = {
        'theme_variables': theme_variables,
        'active_theme': active_theme,
    }
    return render(request, 'myapp/index.html', context)


def theme_list(request):
    """列出所有主题"""
    themes = Theme.objects.all()
    active_theme = Theme.objects.filter(is_active=True).first()
    
    context = {
        'themes': themes,
        'active_theme': active_theme,
    }
    return render(request, 'myapp/theme_list.html', context)


def switch_theme(request, theme_id):
    """切换主题"""
    theme = get_object_or_404(Theme, id=theme_id)
    
    Theme.objects.filter(is_active=True).update(is_active=False)
    
    theme.is_active = True
    theme.save()
    
    messages.success(request, f"已切换到 {theme.name} 主题")
    return redirect('theme_list')


@require_POST
def get_theme_variables(request):
    """获取当前主题的CSS变量"""
    active_theme = Theme.objects.filter(is_active=True).first()
    
    if not active_theme:
        return JsonResponse({'error': '没有激活的主题'}, status=404)
    
    variables = active_theme.variables.all()
    theme_variables = {var.name: var.value for var in variables}
    
    return JsonResponse(theme_variables)


def create_theme(request):
    """创建新主题"""
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'
        
        if is_active:
            Theme.objects.filter(is_active=True).update(is_active=False)
        
        theme = Theme.objects.create(
            name=name,
            code=code,
            description=description,
            is_active=is_active
        )
        
        default_variables = {
            'primary': '#007bff',
            'secondary': '#6c757d',
            'background': '#ffffff',
            'text': '#212529',
            'border': '#dee2e6',
            'shadow': 'rgba(0, 0, 0, 0.1)',
        }
        
        for var_name, var_value in default_variables.items():
            ThemeVariable.objects.create(
                theme=theme,
                name=var_name,
                value=var_value
            )
        
        messages.success(request, f"主题 '{name}' 创建成功")
        return redirect('theme_list')
    
    return redirect('theme_list')


def edit_theme(request, theme_id):
    """编辑主题"""
    theme = get_object_or_404(Theme, id=theme_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        description = request.POST.get('description', '')
        is_active = request.POST.get('is_active') == 'on'
        
        if is_active and not theme.is_active:
            Theme.objects.filter(is_active=True).update(is_active=False)
        
        theme.name = name
        theme.code = code
        theme.description = description
        theme.is_active = is_active
        theme.save()
        
        messages.success(request, f"主题 '{name}' 更新成功")
        return redirect('theme_list')
    
    return redirect('theme_list')


def delete_theme(request, theme_id):
    """删除主题"""
    theme = get_object_or_404(Theme, id=theme_id)
    theme_name = theme.name
    
    if theme.is_active:
        messages.error(request, f"无法删除激活的主题 '{theme_name}'，请先切换到其他主题")
        return redirect('theme_list')
    
    theme.delete()
    
    messages.success(request, f"主题 '{theme_name}' 删除成功")
    return redirect('theme_list')


# ==================== 论坛功能视图 ====================

def forum_index(request):
    """论坛首页 - 显示所有板块"""
    if request.user.is_authenticated and request.user.is_staff:
        forums = Forum.objects.filter(is_active=True)
    else:
        forums = Forum.objects.filter(is_active=True, moderator_only=False)
    
    forum_data = []
    for forum in forums:
        forum_info = {
            'forum': forum,
            'post_count': forum.get_post_count(),
            'last_post': forum.get_last_post(),
        }
        forum_data.append(forum_info)

    unread_notifications_count = 0
    if request.user.is_authenticated:
        unread_notifications_count = Notification.objects.filter(
            recipient=request.user, 
            is_read=False
        ).count()
    
    context = {
        'forums': forum_data,
        'unread_notifications_count': unread_notifications_count,
    }
    return render(request, 'myapp/forum_index.html', context)


def forum_detail(request, forum_id):
    """论坛板块详情 - 显示帖子列表"""
    forum = get_object_or_404(Forum, id=forum_id, is_active=True)
    
    if forum.moderator_only and not (request.user.is_authenticated and request.user.is_staff):
        messages.error(request, "您没有权限访问该板块")
        return redirect('forum_index')
    
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', 'latest')  
    
    posts = Post.objects.filter(forum=forum, is_deleted=False, status='published')
    
    if search:
        posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))
    
    if sort == 'essence':
        posts = posts.filter(is_essence=True)
    elif sort == 'hot':
        posts = posts.order_by('-reply_count', '-view_count', '-created_at')
    else:  
        posts = posts.order_by('-is_top', '-last_reply_at', '-created_at')
    
    paginator = Paginator(posts, 20)  
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    
    context = {
        'forum': forum,
        'posts': posts_page,
        'search': search,
        'sort': sort,
    }
    return render(request, 'myapp/forum_detail.html', context)


@login_required
def post_create(request, forum_id):
    """创建新帖子"""
    forum = get_object_or_404(Forum, id=forum_id, is_active=True)
    
    if forum.moderator_only and not request.user.is_staff:
        messages.error(request, "您没有权限在该板块发帖")
        return redirect('forum_detail', forum_id=forum.id)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        
        if not title or not content:
            messages.error(request, "标题和内容不能为空")
            return redirect('post_create', forum_id=forum.id)
        
        if len(title) > 200:
            messages.error(request, "标题长度不能超过200字符")
            return redirect('post_create', forum_id=forum.id)
        
        post = Post.objects.create(
            forum=forum,
            author=request.user,
            title=title,
            content=content
        )
        
        messages.success(request, "帖子发布成功！")
        return redirect('post_detail', post_id=post.id)
    
    context = {
        'forum': forum,
    }
    return render(request, 'myapp/post_create.html', context)


def post_detail(request, post_id):
    """帖子详情页"""
    post = get_object_or_404(Post, id=post_id, is_deleted=False, status='published')
    
    post.increase_view_count()
    
    replies = post.replies.filter(is_deleted=False).select_related('author', 'parent_reply')
    
    context = {
        'post': post,
        'replies': replies,
    }
    return render(request, 'myapp/post_detail.html', context)


@login_required
def post_edit(request, post_id):
    """编辑帖子"""
    post = get_object_or_404(Post, id=post_id)
    
    if post.author != request.user and not request.user.is_staff:
        messages.error(request, "您没有权限编辑该帖子")
        return redirect('post_detail', post_id=post.id)
    
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        
        if not title or not content:
            messages.error(request, "标题和内容不能为空")
            return redirect('post_edit', post_id=post.id)
        
        post.title = title
        post.content = content
        post.save()
        
        messages.success(request, "帖子更新成功！")
        return redirect('post_detail', post_id=post.id)
    
    context = {
        'post': post,
    }
    return render(request, 'myapp/post_edit.html', context)


@login_required
@require_POST
def post_delete(request, post_id):
    """删除帖子"""
    post = get_object_or_404(Post, id=post_id)
    
    if post.author != request.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'message': '您没有权限删除该帖子'})
    
    post.is_deleted = True
    post.save()
    
    messages.success(request, "帖子已删除")
    return redirect('forum_detail', forum_id=post.forum.id)


@login_required
@require_POST
def add_reply(request, post_id):
    """添加回复"""
    post = get_object_or_404(Post, id=post_id, is_deleted=False)
    content = request.POST.get('content', '').strip()
    parent_reply_id = request.POST.get('parent_reply_id', None)
    
    if not content:
        return JsonResponse({'success': False, 'message': '回复内容不能为空'})
    
    reply_data = {
        'post': post,
        'author': request.user,
        'content': content,
    }
    
    if parent_reply_id:
        try:
            parent_reply = Reply.objects.get(id=parent_reply_id, post=post, is_deleted=False)
            reply_data['parent_reply'] = parent_reply
        except Reply.DoesNotExist:
            pass
    
    reply = Reply.objects.create(**reply_data)
    
    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            sender=request.user,
            notification_type='reply',
            title=f'{request.user.username}回复了您的帖子',
            content=f'《{post.title}》',
            url=post.get_absolute_url()
        )
    
    messages.success(request, "回复成功！")
    return redirect('post_detail', post_id=post.id)


@login_required
@require_POST
def delete_reply(request, reply_id):
    """删除回复"""
    reply = get_object_or_404(Reply, id=reply_id)
    
    if reply.author != request.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'message': '您没有权限删除该回复'})
    
    reply.is_deleted = True
    reply.save()
    
    messages.success(request, "回复已删除")
    return redirect('post_detail', post_id=reply.post.id)


@login_required
def user_profile(request, username=None):
    """用户资料页"""
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    posts_count = Post.objects.filter(author=user, is_deleted=False).count()
    replies_count = Reply.objects.filter(author=user, is_deleted=False).count()
    
    recent_posts = Post.objects.filter(author=user, is_deleted=False, status='published')[:10]
    
    context = {
        'user_profile': user,
        'profile': profile,
        'posts_count': posts_count,
        'replies_count': replies_count,
        'recent_posts': recent_posts,
        'is_own_profile': user == request.user,
    }
    return render(request, 'myapp/user_profile.html', context)


@login_required
def notifications(request):
    """通知列表"""
    notifications = request.user.notifications.order_by('-created_at')
    
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if 'mark_all_read' in request.POST:
            unread_notifications = notifications.filter(is_read=False)
            if unread_notifications.exists():
                unread_notifications.update(is_read=True)
                return JsonResponse({'success': True, 'message': '已标记所有通知为已读'})
            return JsonResponse({'success': True, 'message': '没有未读通知'})
    
    unread_notifications = notifications.filter(is_read=False)
    if unread_notifications.exists():
        unread_notifications.update(is_read=True)
    
    context = {
        'notifications': notifications,
    }
    return render(request, 'myapp/notifications.html', context)


@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """标记通知为已读"""
    try:
        notification = request.user.notifications.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'message': '通知不存在'})


@login_required
@require_POST
def toggle_essence(request, post_id):
    """切换帖子精华状态（管理员功能）"""
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'message': '权限不足'})
    
    try:
        post = Post.objects.get(id=post_id)
        post.is_essence = not post.is_essence
        post.save()
        return JsonResponse({
            'success': True, 
            'is_essence': post.is_essence,
            'message': '已设置为精华帖' if post.is_essence else '已取消精华状态'
        })
    except Post.DoesNotExist:
        return JsonResponse({'success': False, 'message': '帖子不存在'})


# ==================== 用户认证视图 ====================

def signup(request):
    """用户注册视图"""
    if request.user.is_authenticated:
        messages.info(request, "您已登录，无需重复注册")
        return redirect('forum_index')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            
            messages.success(request, f"注册成功！欢迎加入，{user.username}！")
            return redirect('forum_index')
        else:
            messages.error(request, "注册失败，请检查输入信息")
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'registration/signup.html', context)


@login_required
def edit_profile(request):
    """编辑用户资料"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile_form.save()
            
            messages.success(request, "资料更新成功！")
            return redirect('user_profile', username=user.username)
        else:
            messages.error(request, "更新失败，请检查输入信息")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'myapp/edit_profile.html', context)


@login_required
@require_POST
def toggle_top(request, post_id):
    """切换帖子置顶状态（管理员功能）"""
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'message': '权限不足'})
    
    try:
        post = Post.objects.get(id=post_id)
        post.is_top = not post.is_top
        post.save()
        return JsonResponse({
            'success': True, 
            'is_top': post.is_top,
            'message': '帖子已置顶' if post.is_top else '已取消置顶'
        })
    except Post.DoesNotExist:
        return JsonResponse({'success': False, 'message': '帖子不存在'})