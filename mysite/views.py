import datetime
from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.urls import reverse
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,get_yesterday_hot_data
from blog.models import Blog

#用以给首页提供必要的信息
#定义首页
def home(request):
	blog_content_type = ContentType.objects.get_for_model(Blog)
	dates, read_nums = get_seven_days_read_data(blog_content_type)
	#创建了一个context字典
	context = {}
	context['dates'] = dates
	context['read_nums'] = read_nums
	context['today_hot_data'] = get_today_hot_data(blog_content_type)
	context['get_yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
	return render(request, 'home.html',context)





