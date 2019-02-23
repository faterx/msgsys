from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


# 创建意见输入模型
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 意见内容
    text = models.TextField()
    # 意见时间
    comment_time = models.DateTimeField(auto_now=True)
    # 意见提交用户
    user = models.ForeignKey(User,
                             related_name='comments',
                             on_delete=models.CASCADE)
    # 获取一条意见下面所有的回复
    root = models.ForeignKey('self',
                             related_name='root_comment',
                             null=True,
                             on_delete=models.CASCADE)
    # 获取意见的模型
    # 上一级的id
    parent = models.ForeignKey('self',
                               related_name='parent_comment',
                               null=True,
                               on_delete=models.CASCADE)

    # 回复给谁
    reply_to = models.ForeignKey(User,
                                 related_name='replies',
                                 null=True,
                                 on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']


