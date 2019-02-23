# -*- coding:UTF-8 -*-
# Author: Aaron


import datetime

from django.db.models import Sum
from django.shortcuts import *
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse  # 反向解析
from django.utils import timezone
from django.core.cache import cache
from django import forms
from django.views.generic import View

from read_statistics.utils import *
from msg.models import Msg
from .forms import LoginForm, RegForm, AddForm


# 统计一周的查阅数据
def get_7_days_hot_msg():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    msgs = Msg.objects.filter(
        read_details__date__lt=today, read_details__date__gte=date)\
        .values('id', 'created_time') \
        .annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')
    return msgs[:7]

def home(request):
    # msg_content_type = ContentType.objects.get_for_model(Msg)
    # dates, read_nums = get_seven_days_read_data(msg_content_type)

    # 获取7日查询数据
    # hot_msgs_7days = cache.get('hot_msgs_7days')
    # if hot_msgs_7days is None:
    #     hot_msgs_7days = get_7_days_hot_msg()
    #     cache.set('hot_msgs_7days', hot_msgs_7days, 3600)
    #
    # context = {}
    # context['dates'] = dates
    # context['read_nums'] = read_nums
    # context['today_hot_data'] = get_today_hot_data(msg_content_type)
    # context['yesterday_hot_data'] = get_yesterday_hot_data(msg_content_type)
    # context['hot_msgs_7days'] = hot_msgs_7days
    # return render(request, 'home.html', context)
    return render(request, 'home.html')

# 登陆
def login_user(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

# 注册
def registered_user(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']

            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()

            # 登陆用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)

            # 跳转页面
            return redirect(request.GET.get('from', reverse('home')))

    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)

# 登出用户
def logout_user(request):
    logout(request)
    return render(request, 'login.html')

# TODO 添加数据功能存在问题需要进一步修改
# 添加数据
def append_form(request):
    if request.method != 'POST':
        form = AddForm
    else:
        form = AddForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'msg/msg_list.html')

    context = {'form': form}
    return render(request, 'msg/msg_list.html', context)

'''
def append_form(request):
    if request.method == 'POST':
        append_form = AddForm(request.POST)
        if append_form.is_valid():  # 如果各个字段合法
            msg_type = append_form.cleaned_data['msg_type']
            unit = append_form.cleaned_data['unit']
            created_time = append_form.cleaned_data['created_time']
            commander = append_form.cleaned_data['commander']
            commander_phone = append_form.cleaned_data['commander_phone']
            chief_duty = append_form.cleaned_data['chief_duty']
            chief_phone = append_form.cleaned_data['chief_phone']
            operator = append_form.cleaned_data['operator']
            operator_phone = append_form.cleaned_data['operator_phone']
            registered_police = append_form.cleaned_data['registered_police']
            police_duty = append_form.cleaned_data['police_duty']
            emergency_police = append_form.cleaned_data['emergency_police']
            emergency_vehicle = append_form.cleaned_data['emergency_vehicle']
            external_transfer = append_form.cleaned_data['external_transfer']
            num_workers = append_form.cleaned_data['num_workers']
            training_all = append_form.cleaned_data['training_all']
            training_day = append_form.cleaned_data['training_day']
            confinement_all = append_form.cleaned_data['confinement_all']
            confinement_day = append_form.cleaned_data['confinement_day']
            isolation_all = append_form.cleaned_data['isolation_all']
            isolation_day = append_form.cleaned_data['isolation_day']
            death = append_form.cleaned_data['death']
            leave_and_back = append_form.cleaned_data['leave_and_back']
            judicial_all = append_form.cleaned_data['judicial_all']
            judicial_day = append_form.cleaned_data['judicial_day']
            social_all = append_form.cleaned_data['social_all']
            social_day = append_form.cleaned_data['social_day']
            freed_people = append_form.cleaned_data['freed_people']
            parole = append_form.cleaned_data['parole']
            reconfirm = append_form.cleaned_data['reconfirm']
            outside_prison = append_form.cleaned_data['outside_prison']
            outside_prison_death = append_form.cleaned_data['outside_prison_death']
            charter = append_form.cleaned_data['charter']
            detective_relatives_all = append_form.cleaned_data['detective_relatives_all']
            detective_relatives_day = append_form.cleaned_data['detective_relatives_day']
            foreign_workers = append_form.cleaned_data['foreign_workers']
            exotic_vehicle = append_form.cleaned_data['exotic_vehicle']
            video_alarm = append_form.cleaned_data['video_alarm']
            perimeter_alarm = append_form.cleaned_data['perimeter_alarm']
            grid_alarm = append_form.cleaned_data['grid_alarm']
            violation_msg = append_form.cleaned_data['violation_msg']
            leave_prison_msg = append_form.cleaned_data['leave_prison_msg']
            important_msg = append_form.cleaned_data['important_msg']
            emergencies_msg = append_form.cleaned_data['emergencies_msg']
            disposal_msg = append_form.cleaned_data['disposal_msg']

            msg = Msg.objects.create(msg_type=msg_type, unit=unit, created_time=created_time,
                                     commander=commander, commander_phone=commander_phone, chief_duty=chief_duty,
                                     chief_phone=chief_phone, operator=operator, operator_phone=operator_phone,
                                     police_duty=police_duty, police_post=police_post, emergency_police=emergency_police,
                                     emergency_vehicle=emergency_vehicle, external_transfer=external_transfer,
                                     num_workers=num_workers, training_all=training_all, training_day=training_day,
                                     confinement_all=confinement_all, confinement_day=confinement_day, death=death,
                                     isolation_all=isolation_all, isolation_day=isolation_day, judicial_all=judicial_all,
                                     leave_and_back=leave_and_back, judicial_day=judicial_day, social_all=social_all,
                                     social_day=social_day, freed_people=freed_people, parole=parole,
                                     reconfirm=reconfirm, outside_prison=outside_prison, charter=charter,
                                     outside_prison_death=outside_prison_death, police_on_pos=police_on_post,
                                     detective_relatives_all=detective_relatives_all, exotic_vehicle=exotic_vehicle,
                                     detective_relatives_day=detective_relatives_day, violation_msg=violation_msg,
                                     video_alarm=video_alarm, perimeter_alarm=perimeter_alarm, grid_alarm=grid_alarm,
                                     leave_prison_msg=leave_prison_msg, disposal_msg=disposal_msg,
                                     important_msg=important_msg, emergencies_msg=emergencies_msg)
            msg.save()

            return redirect(request.GET.get('from', reverse('home')))

    else:
        append_form = AddForm()

    context = {}
    context['append_form'] = append_form
    return render(request, 'msg_write.html', context)
'''

'''
# 文件上传
import os
# 使用此方法需要在form表单中添加enctype="multipart/form-data"
def upload_file(request):
    if request.method == 'POST'
        obj = request.FILES.get('form表单的name')
        file_path = os.path.join('media/upload', obj.name)
        # 打开文件
        f = open(obj.name, mode='wb')
        for item in obj.chunks():
            f.write(item)
        f.close()
    return render(request, '指定页面')
    # 获取多选数据使用request.POST.getlist('表单名称')
'''