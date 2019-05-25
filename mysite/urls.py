"""mysite URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin    #导入Admin功能模块
from django.urls import include, path#如果路径和转换器语法不足以定义URL模式，则还可以使用正则表达式。为此，请引用re_path()而不是path()
from django.conf import settings    #
from django.conf.urls.static import static
from . import views #

#urlpatterns应该是一个序列的path() 和/或re_path()实例
urlpatterns = [
    #path(route, view, kwargs=None, name=None)模块
    path('', views.home, name='home'),  ##首页地址，同层目录下views.py中的home函数，此url为命名为home，用于在html中使用
    #include()当您包含其他URL模式时，应始终使用。 admin.site.urls是唯一的例外。
    path('admin/', admin.site.urls),    #'admin/'代表127.0.0.1：8000/admin地址信息，admin.site.urls是URL的处理函数，也称为视图函数
    path('ckeditor', include('ckeditor_uploader.urls')), #？富文本标签应该怎么理解
    path('blog/', include('blog.urls')), #include将该URL分配给blog的urls.py处理
    path('comment/', include('comment.urls')),#include将该URL分配给comment的urls.py处理
    path('likes/', include('likes.urls')),#include将该URL分配给like的urls.py处理
    path('user/', include('user.urls')),#include将该URL分配给user的urls.py处理
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #?？？