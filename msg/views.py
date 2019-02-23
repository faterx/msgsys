from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count

from .models import Msg, MsgType
from read_statistics.utils import read_statistics_once_read


def get_msg_list_common_data(request, msgs_all_list):
    paginator = Paginator(msgs_all_list, settings.EACH_PAGE_MSGS_NUMBER)
    # 获取页码参数(使用GET请求）
    page_num = request.GET.get('page', 1)
    # 获取页码的类型，自动识别
    page_of_msgs = paginator.get_page(page_num)
    # 获取当前页码 (dy1)
    currentr_page_num = page_of_msgs.number
    # 获取前后各两页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 > 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    '''
    # 获取数据分类的对应数据数量dy2(方法一)
    msg_types = MsgType.objects.all()
    msg_types_list = []
    for msg_type in msg_types:
        msg_type.msg_count = Msg.objects.filter(msg_type=msg_type).count()
        msg_types_list.append(msg_type)
    '''

    # 获取信息分类的对应数量dy2(方法二)
    # MsgType.objects.annotate(msg_count=Count('msg'))

    # 跳转第一页或者最后一页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取日期分类统计数量
    msg_dates = Msg.objects.dates('created_time', 'month', order='DESC')
    msg_dates_dict = {}
    for msg_date in msg_dates:
        msg_count = Msg.objects.filter(created_time__year=msg_date.year,
                                       created_time__month=msg_date.month).count()
        msg_dates_dict[msg_date] = msg_count

    context = {}
    context['msgs'] = page_of_msgs.object_list
    context['page_of_msgs'] = page_of_msgs
    context['page_range'] = page_range  # (dy1)
    # context['msg_types'] = MsgType.objects.all()
    # context['msg_types'] = msg_types_list  # dy2
    context['msg_types'] = MsgType.objects.annotate(msg_count=Count('msg'))  # dy2(方法二）
    # context['msg_dates'] = Msg.objects.dates('created_time', 'month', order='DESC')
    context['msg_dates'] = msg_dates_dict  # dy2
    return context


def msg_list(request):
    # 获取全部数据
    msgs_all_list = Msg.objects.all()
    context = get_msg_list_common_data(request, msgs_all_list)
    return render(request, 'msg/msg_list.html', context)


def msg_with_type(request, msg_type_pk):
    msg_type = get_object_or_404(MsgType, pk=msg_type_pk)
    msgs_all_list = Msg.objects.filter(msg_type=msg_type)
    context = get_msg_list_common_data(request, msgs_all_list)
    context['msg_type'] = msg_type
    return render(request, 'msg/msg_with_type.html', context)


def msgs_with_date(request, year, month):
    msgs_all_list = Msg.objects.filter(created_time__year=year, created_time__month=month)
    context = get_msg_list_common_data(request, msgs_all_list)
    context['msgs_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'msg/msgs_with_data.html', context)


def msg_detail(request, msg_pk):
    msg = get_object_or_404(Msg, pk=msg_pk)
    read_cookie_key = read_statistics_once_read(request, msg)

    context = {}
    # 去当前打开的这篇数据并找到时间进行比较，取到上一条数据
    context['previous_msg'] = Msg.objects.filter(
                                created_time__gt=msg.created_time).last()
    # 下一条数据
    context['next_msg'] = Msg.objects.filter(created_time__lt=msg.created_time).first()
    # 当前数据
    context['msg'] = msg

    response = render(request, 'msg/msg_detail.html', context)  # 响应
    response.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记，告诉浏览器保存信息 类似字典
    return response
