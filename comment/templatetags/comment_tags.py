from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment#引用上一层文件夹
from ..forms import CommentForm#在上级目录中引用CommentForm


register = template.Library()

@register.simple_tag
def get_comment_count(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()#.pk是获取obj的组件值

#注册标签
@register.simple_tag
#获取评论表单
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    #初始化
    form = CommentForm(initial={
            'content_type': content_type.model, 
            'object_id': obj.pk, 
            'reply_comment_id': 0})
    return form


#获取某一篇博客的具体列表
@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-comment_time')