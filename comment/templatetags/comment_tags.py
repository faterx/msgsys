# -*- coding:UTF-8 -*-
# Author:Liux


from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment  # 一个点是当前文件夹，两个点是上一层文件夹
from ..froms import CommentForm


register = template.Library()

@register.simple_tag()
def get_comment_count(obj):
    # 通过筛选出回复总数后计数并返回给前端页面
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(
                        content_type=content_type,
                        object_id=obj.pk).count()

@register.simple_tag()
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={
                        'content_type': content_type.model,
                        'object_id': obj.pk,
                        'reply_comment_id': '0'})
    return form

# 返回意见数据给当前前端页面
@register.simple_tag()
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    # 获取意见的数据
    comments = Comment.objects.filter(content_type=content_type,
                                      object_id=obj.pk,
                                      parent=None)
    return comments.order_by('-comment_time')
