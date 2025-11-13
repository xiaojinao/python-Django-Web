from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import strip_tags
from django.urls import reverse


class Theme(models.Model):
    """
    主题模型，用于存储网站主题配置
    """
    name = models.CharField(max_length=50, verbose_name="主题名称")
    identifier = models.CharField(max_length=20, unique=True, verbose_name="主题标识符")
    is_active = models.BooleanField(default=False, verbose_name="是否激活")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "主题"
        verbose_name_plural = "主题"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # 确保只有一个主题是激活状态
        if self.is_active:
            Theme.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)


class ThemeVariable(models.Model):
    """
    主题变量模型，用于存储每个主题的CSS变量
    """
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='variables', verbose_name="所属主题")
    name = models.CharField(max_length=50, verbose_name="变量名")
    value = models.CharField(max_length=100, verbose_name="变量值")
    
    class Meta:
        verbose_name = "主题变量"
        verbose_name_plural = "主题变量"
        unique_together = ('theme', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.theme.name} - {self.name}"


# ==================== 论坛功能模型 ====================

class Forum(models.Model):
    """
    论坛板块模型
    """
    ORDER_CHOICES = [
        (1, '第1位'),
        (2, '第2位'),
        (3, '第3位'),
        (4, '第4位'),
        (5, '第5位'),
    ]
    
    name = models.CharField(max_length=50, verbose_name="板块名称")
    description = models.TextField(blank=True, verbose_name="板块描述")
    icon = models.CharField(max_length=100, blank=True, verbose_name="板块图标")
    order = models.IntegerField(choices=ORDER_CHOICES, default=1, verbose_name="排序")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")
    moderator_only = models.BooleanField(default=False, verbose_name="仅管理员可见")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "论坛板块"
        verbose_name_plural = "论坛板块"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_post_count(self):
        """获取板块内的帖子总数"""
        return self.posts.filter(is_deleted=False).count()
    
    def get_last_post(self):
        """获取板块内最新的帖子"""
        return self.posts.filter(is_deleted=False).order_by('-created_at').first()


class Post(models.Model):
    """
    帖子模型
    """
    STATUS_CHOICES = [
        ('published', '已发布'),
        ('draft', '草稿'),
        ('hidden', '已隐藏'),
    ]
    
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name='posts', verbose_name="所属板块")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name="作者")
    title = models.CharField(max_length=200, verbose_name="帖子标题")
    content = models.TextField(verbose_name="帖子内容")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published', verbose_name="状态")
    is_top = models.BooleanField(default=False, verbose_name="是否置顶")
    is_essence = models.BooleanField(default=False, verbose_name="是否精华")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    view_count = models.IntegerField(default=0, verbose_name="浏览次数")
    reply_count = models.IntegerField(default=0, verbose_name="回复次数")
    last_reply_at = models.DateTimeField(blank=True, null=True, verbose_name="最后回复时间")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "帖子"
        verbose_name_plural = "帖子"
        ordering = ['-is_top', '-last_reply_at', '-created_at']
    
    def __str__(self):
        return self.title
    
    def get_excerpt(self, length=100):
        """获取帖子内容摘要"""
        content = strip_tags(self.content)
        if len(content) <= length:
            return content
        return content[:length] + '...'
    
    def increase_view_count(self):
        """增加浏览次数"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    def update_reply_count(self):
        """更新回复数量"""
        self.reply_count = self.replies.filter(is_deleted=False).count()
        if self.reply_count > 0:
            self.last_reply_at = self.replies.latest('created_at').created_at
        self.save(update_fields=['reply_count', 'last_reply_at'])
    
    def get_absolute_url(self):
        """获取帖子的绝对URL"""
        return reverse('post_detail', kwargs={'post_id': self.id})


class Reply(models.Model):
    """
    回复模型
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies', verbose_name="所属帖子")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies', verbose_name="作者")
    content = models.TextField(verbose_name="回复内容")
    parent_reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, 
                                   related_name='child_replies', verbose_name="父回复")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "回复"
        verbose_name_plural = "回复"
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.author.username}的回复"
    
    def get_excerpt(self, length=50):
        """获取回复内容摘要"""
        content = strip_tags(self.content)
        if len(content) <= length:
            return content
        return content[:length] + '...'


class UserProfile(models.Model):
    """
    用户资料模型，扩展Django自带的User模型
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="用户")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="头像")
    bio = models.TextField(blank=True, verbose_name="个人简介")
    signature = models.CharField(max_length=100, blank=True, verbose_name="个性签名")
    post_count = models.IntegerField(default=0, verbose_name="发帖数")
    reply_count = models.IntegerField(default=0, verbose_name="回复数")
    reputation = models.IntegerField(default=0, verbose_name="声望值")
    last_login_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="最后登录IP")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    class Meta:
        verbose_name = "用户资料"
        verbose_name_plural = "用户资料"
    
    def __str__(self):
        return f"{self.user.username}的资料"
    
    def increase_post_count(self):
        """增加发帖数"""
        self.post_count += 1
        self.save(update_fields=['post_count'])
    
    def increase_reply_count(self):
        """增加回复数"""
        self.reply_count += 1
        self.save(update_fields=['reply_count'])
    
    def calculate_reputation(self):
        """计算声望值"""
        # 声望值计算规则：发帖数 * 2 + 回复数 * 1 + 精华帖 * 10
        essence_bonus = Post.objects.filter(
            author=self.user, 
            is_essence=True, 
            is_deleted=False
        ).count() * 10
        
        self.reputation = self.post_count * 2 + self.reply_count + essence_bonus
        self.save(update_fields=['reputation'])


class Notification(models.Model):
    """
    通知模型
    """
    NOTIFICATION_TYPES = [
        ('reply', '回复'),
        ('mention', '提及'),
        ('system', '系统通知'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name="接收者")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='sent_notifications', verbose_name="发送者")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, verbose_name="通知类型")
    title = models.CharField(max_length=200, verbose_name="通知标题")
    content = models.TextField(verbose_name="通知内容")
    url = models.CharField(max_length=200, blank=True, verbose_name="跳转链接")
    is_read = models.BooleanField(default=False, verbose_name="是否已读")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name = "通知"
        verbose_name_plural = "通知"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.recipient.username} - {self.title}"


# ==================== 模型信号处理 ====================

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """当创建用户时自动创建用户资料"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """当保存用户时保存用户资料"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(post_save, sender=Post)
def update_post_count(sender, instance, created, **kwargs):
    """发帖时更新用户统计"""
    if created and not instance.is_deleted:
        profile = instance.author.profile
        profile.increase_post_count()
        profile.calculate_reputation()


@receiver(post_delete, sender=Post)
def decrease_post_count(sender, instance, **kwargs):
    """删帖时更新用户统计"""
    if not instance.is_deleted:
        profile = instance.author.profile
        profile.post_count = max(0, profile.post_count - 1)
        profile.calculate_reputation()
        profile.save()


@receiver(post_save, sender=Reply)
def update_reply_count(sender, instance, created, **kwargs):
    """回复时更新用户和帖子统计"""
    if created and not instance.is_deleted:
        # 更新回复者的统计
        profile = instance.author.profile
        profile.increase_reply_count()
        profile.calculate_reputation()
        
        # 更新帖子的回复数
        post = instance.post
        post.update_reply_count()
    
    elif not created:
        # 删除回复时更新统计
        profile = instance.author.profile
        profile.reply_count = max(0, profile.reply_count - 1)
        profile.calculate_reputation()
        profile.save()