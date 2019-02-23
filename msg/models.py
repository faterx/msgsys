from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail


# 内容分类
class MsgType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

# 内容主体
class Msg(models.Model, ReadNumExpandMethod):
    # 内容分类
    msg_type = models.ForeignKey(MsgType, on_delete=models.CASCADE)
    # 单位
    unit = models.CharField(max_length=10)
    # 创建时间
    created_time = models.DateTimeField(default=False)
    # 操作员
    Operator = models.ForeignKey(User, on_delete=models.CASCADE)
    # 指挥长
    commander = models.CharField(max_length=5)
    commander_phone = models.CharField(max_length=15)
    # 值班长
    chief_duty = models.CharField(max_length=5)
    chief_phone = models.CharField(max_length=15)
    # 值班员
    operator = models.CharField(max_length=5)
    operator_phone = models.CharField(max_length=15)
    # 在册民警
    registered_police = models.CharField(max_length=5)
    # 值班民警
    police_duty = models.CharField(max_length=5)
    # 应急民警
    emergency_police = models.CharField(max_length=5)
    # 应急车辆
    emergency_vehicle = models.CharField(max_length=5)
    # 新收罪犯
    external_transfer = models.CharField(max_length=5)
    # 出工人数
    num_workers = models.CharField(max_length=5)
    # 集训
    training_all = models.CharField(max_length=5)
    training_day = models.CharField(max_length=5)
    # 禁闭
    confinement_all = models.CharField(max_length=5)
    confinement_day = models.CharField(max_length=5)
    # 隔离审查
    isolation_all = models.CharField(max_length=5)
    isolation_day = models.CharField(max_length=5)
    # 罪犯死亡
    death = models.CharField(max_length=5)
    # 离监就医
    leave_and_back = models.CharField(max_length=5)
    # 司法医院
    judicial_all = models.CharField(max_length=5)
    judicial_day = models.CharField(max_length=5)
    # 社会医院
    social_all = models.CharField(max_length=5)
    social_day = models.CharField(max_length=5)
    # 刑满释放
    freed_people = models.CharField(max_length=5)
    # 假释出监
    parole = models.CharField(max_length=5)
    # 解回再审
    reconfirm = models.CharField(max_length=5)
    # 暂予监外执行
    outside_prison = models.CharField(max_length=5)
    # 暂予监外执行死亡
    outside_prison_death = models.CharField(max_length=5)
    # 特许离监
    charter = models.CharField(max_length=5)
    # 离监探亲
    detective_relatives_all = models.CharField(max_length=5)
    detective_relatives_day = models.CharField(max_length=5)
    # 外来人员进监
    foreign_workers = models.CharField(max_length=5)
    # 外来车辆进监
    exotic_vehicle = models.CharField(max_length=5)
    # 视频事件报警
    video_alarm = models.CharField(max_length=5)
    # 周界报警
    perimeter_alarm = models.CharField(max_length=5)
    # 电网报警
    grid_alarm = models.CharField(max_length=5)
    # 违规违纪
    violation_msg = RichTextUploadingField()
    # 罪犯出监
    leave_prison_msg = RichTextUploadingField()
    # 其他重要信息
    important_msg = RichTextUploadingField()
    # 突发事件
    emergencies_msg = RichTextUploadingField()
    # 处置状态
    disposal_msg = RichTextUploadingField()
    # 最后修改事件
    last_updated_time = models.DateTimeField(auto_now=True)

    # 关联数据模型，便于访问
    read_details = GenericRelation(ReadDetail)

    def __str__(self):
        return '<Msg: %s>' % self.created_time

    class Meta:
        ordering = ['-created_time']
