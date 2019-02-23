"""msgsys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # dy2
from django.conf.urls.static import static  # dy2生产环境部署不要使用
from . import views


def i18n_javascript(request):
    return admin.site.i18n_javascript(request)

urlpatterns = [
    path('', views.login_user, name='login'),
    path('admin/jsi18n', i18n_javascript),
    path('admin/', admin.site.urls),
    path('ckeditor', include('ckeditor_uploader.urls')),  # dy2
    path('msg/', include('msg.urls')),
    path('comment/', include('comment.urls')),
    path('home/', views.home, name='home'),
    path('register/', views.registered_user, name='register'),
    path('add/', views.append_form, name='add'),
]

# 后面的值是能够访问这个路径（开发环境使用的方法，部署环境的时候不要使用）
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 路由写法推荐以下方式：
# url(r'^网址名称-(?P<自己赋值>\d+)-(?P<自己赋值2>).html', views.detail)
# 配套函数使用：
# def detail(request, *args, **kwargs):
#     pass

