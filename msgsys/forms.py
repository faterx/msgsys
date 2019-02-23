# -*- coding:UTF-8 -*-
# Author: Aaron


from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.admin import widgets
from ckeditor.widgets import CKEditorWidget

from msg.models import Msg, MsgType


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput(
                                            attrs={'class': 'form-control',
                                                   'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(
                                            attrs={'class': 'form-control',
                                                   'placeholder': '请输入密码'}))

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码错误!')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(
                     label='用户名',
                     max_length=10, min_length=3,
                     widget=forms.TextInput(
                                  attrs={'class': 'form-control',
                                         'placeholder': '请输入3-10位的用户名'}))

    email = forms.EmailField(
                  label='邮箱',
                  widget=forms.EmailInput(
                               attrs={'class': 'form-control',
                                      'placeholder': '请输入邮箱地址'}))

    password = forms.CharField(
                     label='密码',
                     min_length=6,
                     widget=forms.PasswordInput(
                                  attrs={'class': 'form-control',
                                         'placeholder': '请输入密码'}))

    password_again = forms.CharField(
                           label='密码',
                           min_length=6,
                           widget=forms.PasswordInput(
                                        attrs={'class': 'form-control',
                                               'placeholder': '请再次输入密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在！')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱地址已存在！')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致!')
        return password_again

class LogoutForm(forms.Form):
    pass

"""
class AddForm(forms.ModelForm):
    class Meta:
        model = Msg
        exclude = ['last_updated_time', 'read_details']
        '''
        fields = ['msg_type', 'unit', 'created_time', 'Operator', 'commander',
                  'commander_phone', 'chief_duty', 'chief_phone', 'operator',
                  'operator_phone', 'registered_police', 'police_duty',
                  'emergency_police', 'emergency_vehicle', 'external_transfer',
                  'num_workers', 'training_all', 'training_day',  'confinement_all',
                  'confinement_day', 'isolation_all', 'isolation_day', 'death',
                  'leave_and_back', 'judicial_all', 'judicial_day', 'social_all',
                  'social_day', 'freed_people', 'parole', 'reconfirm',
                  'outside_prison', 'outside_prison_death', 'charter',
                  'detective_relatives_all', 'detective_relatives_day',
                  'foreign_workers', 'exotic_vehicle', 'video_alarm',
                  'perimeter_alarm', 'grid_alarm', 'violation_msg', 'leave_prison_msg',
                  'important_msg', 'emergencies_msg', 'disposal_msg']
                  '''
        # 添加标签
        labels = {'msg_type': '信息类别', 'unit': '填报单位', 'created_time': '填报时间',
                  'Operator': '填报人',  'commander': '指挥长', 'commander_phone': '联系电话',
                  'chief_duty': '值班长', 'chief_phone': '联系电话', 'operator': '值班员',
                  'operator_phone': '联系电话', 'registered_police': '在册民警',
                  'police_duty': '值班民警', 'emergency_police': '应急民警',
                  'emergency_vehicle': '应急车辆', 'external_transfer': '外系统(省)送入新收押犯数',
                  'num_workers': '出工人数', 'training_all': '全监集训总数',
                  'training_day': '当日集训发生数', 'confinement_all': '全监禁闭数',
                  'confinement_day': '当日禁闭发生数', 'isolation_all': '全监隔离审查数',
                  'isolation_day': '隔离审查当日发生', 'death': '罪犯死亡',
                  'leave_and_back': '离监就医当日返监', 'judicial_all': '司法医院住院总数',
                  'judicial_day': '司法医院当日住院', 'social_all': '社会医院住院总数',
                  'social_day': '社会医院住院总数', 'freed_people': '刑满释放',
                  'parole': '刑满释放', 'reconfirm': '假释出监', 'outside_prison': '暂予监外执行',
                  'outside_prison_death': '监外执行罪犯死亡', 'charter': '特许离监',
                  'detective_relatives_all': '离监探亲全监总数',
                  'detective_relatives_day': '离监谈情当日发生',
                  'foreign_workers': '外来人员进监', 'exotic_vehicle': '外来车辆进监',
                  'video_alarm': '视频事件报警', 'perimeter_alarm': '周界报警', 'grid_alarm': '电网报警',
                  'violation_msg': '违规违纪', 'leave_prison_msg': '罪犯出监',
                  'important_msg': '其他重要信息', 'emergencies_msg': '突发事件', 'disposal_msg': '处置状态'}

        # 修改html中的某些样式
        widgets = {
            'violation_msg': forms.Textarea(attrs={'row': 4,
                                                   'placeholder': '200字以内'}),
            'leave_prison_msg': forms.Textarea(attrs={'row': 4,
                                                      'placeholder': '200字以内'}),
            'important_msg': forms.Textarea(attrs={'row': 4,
                                                   'placeholder': '200字以内'}),
            'emergencies_msg': forms.Textarea(attrs={'row': 4,
                                                     'placeholder': '200字以内'}),
            'disposal_msg': forms.Textarea(attrs={'row': 4,
                                                  'placeholder': '200字以内'}),
        }
"""


class AddForm(forms.Form):
    FORMAT_YEAR = ['%Y-%m-%d']
    CHOICEFILES = MsgType.objects.filter(msg_type='msg_type').all()
    msg_type = forms.ChoiceField(label='内容分类',  # 需要能够选择
                                 choices=CHOICEFILES,
                                 widget=forms.Select(
                                       attrs={'class': 'form-control'}))

    unit = forms.CharField(label='填报单位',
                           max_length=10, min_length=4,
                           widget=forms.TextInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': 'XX单位'}))

    created_time = forms.DateField(label='填报时间',
                                   input_formats=FORMAT_YEAR,
                                   widget=forms.SelectDateWidget(
                                         attrs={'class': 'form-control',
                                                'placeholder': '日期格式：xxxx-xx-xx'}))

    commander = forms.CharField(label='指挥长',
                                min_length=1, max_length=5,
                                widget=forms.TextInput(
                                      attrs={'class': 'form-control'}))
    commander_phone = forms.CharField(label='联系电话',
                                      widget=forms.NumberInput(
                                            attrs={'class': 'form-control'}))

    chief_duty = forms.CharField(label='值班长',
                                 min_length=1, max_length=5,
                                 widget=forms.TextInput(
                                       attrs={'class': 'form-control'}))
    chief_phone = forms.CharField(label='联系电话',
                                  widget=forms.NumberInput(
                                        attrs={'class': 'form-control'}))

    operator = forms.CharField(label='值班员',
                               max_length=5, min_length=1,
                               widget=forms.TextInput(
                                     attrs={'class': 'form-control'}))
    operator_phone = forms.CharField(label='联系电话',
                                     widget=forms.NumberInput(
                                           attrs={'class': 'form-control'}))

    registered_police = forms.CharField(label='在册民警',
                                        max_length=5,
                                        widget=forms.NumberInput(
                                              attrs={'class': 'form-control'}))

    police_duty = forms.CharField(label='值班民警',
                                  max_length=5,
                                  widget=forms.NumberInput(
                                        attrs={'class': 'form-control'}))

    emergency_police = forms.CharField(label='应急民警',
                                       max_length=5,
                                       widget=forms.NumberInput(
                                             attrs={'class': 'form-control'}))

    emergency_vehicle = forms.CharField(label='应急车辆',
                                        max_length=5,
                                        widget=forms.NumberInput(
                                              attrs={'class': 'form-control'}))

    external_transfer = forms.CharField(label='外系统(省)送入新收押犯数',
                                        max_length=5,
                                        widget=forms.NumberInput(
                                              attrs={'class': 'form-control'}))

    num_workers = forms.CharField(label='出工人数',
                                  max_length=5,
                                  widget=forms.NumberInput(
                                        attrs={'class': 'form-control'}))

    training_all = forms.CharField(label='集训全监总数',
                                   max_length=5,
                                   widget=forms.NumberInput(
                                         attrs={'class': 'form-control'}))
    training_day = forms.CharField(label='集训当日发生',
                                   max_length=5,
                                   widget=forms.NumberInput(
                                         attrs={'class': 'form-control'}))

    confinement_all = forms.CharField(label='禁闭全监总数',
                                      max_length=5,
                                      widget=forms.NumberInput(
                                            attrs={'class': 'form-control'}))
    confinement_day = forms.CharField(label='禁闭当日发生',
                                      max_length=5,
                                      widget=forms.NumberInput(
                                            attrs={'class': 'form-control'}))

    isolation_all = forms.CharField(label='隔离审查全监总数',
                                    max_length=5,
                                    widget=forms.NumberInput(
                                          attrs={'class': 'form-control'}))
    isolation_day = forms.CharField(label='隔离审查当日发生',
                                    max_length=5,
                                    widget=forms.NumberInput(
                                          attrs={'class': 'form-control'}))

    death = forms.CharField(label='罪犯死亡',
                            max_length=5,
                            widget=forms.NumberInput(
                                  attrs={'class': 'form-control'}))

    leave_and_back = forms.CharField(label='离监就医当日返监',
                                     max_length=5,
                                     widget=forms.NumberInput(
                                           attrs={'class': 'form-control'}))

    judicial_all = forms.CharField(label='司法医院住院总数',
                                   max_length=5,
                                   widget=forms.NumberInput(
                                         attrs={'class': 'form-control'}))
    judicial_day = forms.CharField(label='司法医院当日住院',
                                   max_length=5,
                                   widget=forms.NumberInput(
                                         attrs={'class': 'form-control'}))

    social_all = forms.CharField(label='社会医院住院总数',
                                 max_length=5,
                                 widget=forms.NumberInput(
                                       attrs={'class': 'form-control'}))
    social_day = forms.CharField(label='社会医院当日住院',
                                 max_length=5,
                                 widget=forms.NumberInput(
                                       attrs={'class': 'form-control'}))

    freed_people = forms.CharField(label='刑满释放',
                                   max_length=5,
                                   widget=forms.NumberInput(
                                         attrs={'class': 'form-control'}))

    parole = forms.CharField(label='假释出监',
                             max_length=5,
                             widget=forms.NumberInput(
                                   attrs={'class': 'form-control'}))

    reconfirm = forms.CharField(label='解回再审',
                                max_length=5,
                                widget=forms.NumberInput(
                                      attrs={'class': 'form-control'}))

    outside_prison = forms.CharField(label='暂予监外执行',
                                     max_length=5,
                                     widget=forms.NumberInput(
                                           attrs={'class': 'form-control'}))

    outside_prison_death = forms.CharField(label='监外执行罪犯死亡',
                                           max_length=5,
                                           widget=forms.NumberInput(
                                               attrs={'class': 'form-control'}))

    charter = forms.CharField(label='特许离监',
                              max_length=5,
                              widget=forms.NumberInput(
                                    attrs={'class': 'form-control'}))

    detective_relatives_all = forms.CharField(label='离监探亲全监总数',
                                              max_length=5,
                                              widget=forms.NumberInput(
                                                    attrs={'class': 'form-control'}))
    detective_relatives_day = forms.CharField(label='离监探亲当日发生',
                                              max_length=5,
                                              widget=forms.NumberInput(
                                                    attrs={'class': 'form-control'}))

    foreign_workers = forms.CharField(label='外来人员进监',
                                      max_length=5,
                                      widget=forms.NumberInput(
                                            attrs={'class': 'form-control'}))

    exotic_vehicle = forms.CharField(label='外来车辆进监',
                                     max_length=5,
                                     widget=forms.NumberInput(
                                           attrs={'class': 'form-control'}))

    video_alarm = forms.CharField(label='视频事件报警',
                                  max_length=5,
                                  widget=forms.NumberInput(
                                        attrs={'class': 'form-control'}))

    perimeter_alarm = forms.CharField(label='周界报警',
                                      max_length=5,
                                      widget=forms.NumberInput(
                                            attrs={'class': 'form-control'}))

    grid_alarm = forms.CharField(label='电网报警',
                                 max_length=5,
                                 widget=forms.NumberInput(
                                       attrs={'class': 'form-control'}))

    violation_msg = forms.CharField(label='违规违纪',
                                    max_length=200, min_length=1,
                                    widget=forms.Textarea(
                                          attrs={'class': 'form-control', 'row': '4',
                                                 'placeholder': '200字以内'}),
                                    error_messages={'required': '内容不能为空！'})

    leave_prison_msg = forms.CharField(label='罪犯出监',
                                       max_length=200, min_length=1,
                                       widget=forms.Textarea(
                                           attrs={'class': 'form-control', 'row': '4',
                                                  'placeholder': '200字以内'}),
                                       error_messages={'required': '内容不能为空！'})

    important_msg = forms.CharField(label='其他重要信息',
                                    max_length=200, min_length=1,
                                    widget=forms.Textarea(
                                           attrs={'class': 'form-control', 'row': '4',
                                                  'placeholder': '200字以内'}),
                                    error_messages={'required': '内容不能为空！'})

    emergencies_msg = forms.CharField(label='突发事件',
                                      max_length=200, min_length=1,
                                      widget=forms.Textarea(
                                            attrs={'class': 'form-control', 'row': '4',
                                                   'placeholder': '200字以内'}),
                                      error_messages={'required': '内容不能为空！'})

    disposal_msg = forms.CharField(label='处置状态',
                                   max_length=200, min_length=1,
                                   widget=forms.Textarea(
                                         attrs={'class': 'form-control', 'row': '4',
                                                'placeholder': '200字以内'}),
                                   error_messages={'required': '内容不能为空！'})

    def clean_created_time(self):
        created_time = self.cleaned_data['created_time']
        if Msg.objects.filter(created_time=created_time).exists():
            raise forms.ValidationError('此记录已经存在，请在系统中查询！')
        return created_time
