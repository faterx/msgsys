# -*- coding:UTF-8 -*-
# Author: Liux


from django.urls import path
from . import views


urlpatterns = [

    # 获取连接为127.0.0.1:8000/msg/?的页面
    path('', views.msg_list, name='msg_list'),
    path('<int:msg_pk>', views.msg_detail, name='msg_detail'),
    path('type/<int:msg_type_pk>', views.msg_with_type, name='msg_whit_type'),
    path('date/<int:year>/<int:month>', views.msgs_with_date, name='msgs_with_data'),

]