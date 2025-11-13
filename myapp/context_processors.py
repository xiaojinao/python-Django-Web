from django.contrib.auth.decorators import login_required

def notification_count(request):
    """
    为模板提供当前用户的未读通知数量
    """
    if request.user.is_authenticated:
        from .models import Notification
        unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return {
            'unread_notification_count': unread_count
        }
    return {
        'unread_notification_count': 0
    }